import logging
import pandas as pd
from django.db import transaction
from drawranflow.models import Identifiers, Message
from django.core.exceptions import ObjectDoesNotExist
from .utils import save_messages


def process_e1ap_dataframe(df, item_id, interface):
    try:
        e1ap_df = df[df['frame.protocols'].apply(lambda x: 'e1ap' in x.lower() if isinstance(x, str) else False)]
        e1ap_df.loc[:, 'e1ap.GNB_CU_CP_UE_E1AP_ID'] = e1ap_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].astype(str)
        e1ap_df.loc[:, 'e1ap.GNB_CU_UP_UE_E1AP_ID'] = e1ap_df['e1ap.GNB_CU_UP_UE_E1AP_ID'].astype(str)
        grouped_df = e1ap_df.groupby('e1ap.GNB_CU_CP_UE_E1AP_ID')

        with transaction.atomic():
            for _, group_df in grouped_df:
                try:
                    logging.debug(
                        f"Processing E1AP messages for GNB_CU_CP_UE_E1AP_ID: {group_df['e1ap.GNB_CU_CP_UE_E1AP_ID'].iloc[0]}")
                    process_bearer_context_setup_request(group_df, item_id, interface)
                    process_bearer_context_setup_response(group_df, item_id, interface)
                    process_other_e1ap_messages(group_df, item_id, interface)
                except Exception as e:
                    logging.error(f"Error processing group: {e}")
    except Exception as e:
        logging.error(f"Error processing e1ap dataframe: {e}")


def process_bearer_context_setup_request(df, item_id, interface):
    try:
        df_filtered = df[df['_ws.col.info'] == 'BearerContextSetupRequest']
        with transaction.atomic():
            for index, row in df_filtered.iterrows():
                gnb_cu_cp_ue_e1ap_id = row['e1ap.GNB_CU_CP_UE_E1AP_ID']
                logging.info(
                    f"E1AP-BearerContextSetupRequest: row: {index}, Message: {row['_ws.col.info']}, gnb_cu_cp_ue_e1ap_id: {gnb_cu_cp_ue_e1ap_id}")
                try:
                    identifier_object = Identifiers.objects.get(
                        GNB_CU_UE_F1AP_ID=gnb_cu_cp_ue_e1ap_id,
                        GNB_CU_CP_UE_E1AP_ID__isnull=True,
                        GNB_CU_UP_UE_E1AP_ID__isnull=True,
                        uploadedFiles_id=item_id
                    )

                    rrc_setup_complete_exists = Message.objects.filter(
                        identifiers_id=identifier_object.id,
                        Message__iexact='Service request'.strip(),
                        Protocol__icontains='ngap'
                    ).exists()

                    rrc_reg_complete_exists = Message.objects.filter(
                        identifiers_id=identifier_object.id,
                        Message__iexact='Registration request'.strip(),
                        Protocol__icontains='ngap'
                    ).exists()

                    if rrc_setup_complete_exists or rrc_reg_complete_exists:
                        identifier_object.GNB_CU_CP_UE_E1AP_ID = gnb_cu_cp_ue_e1ap_id
                        identifier_object.save()
                        save_messages(row, identifier_object, interface)

                except Identifiers.DoesNotExist:
                    logging.error(f"Identifier does not exist. {row['frame.number']}-{row['_ws.col.info']}")
                except Exception as e:
                    logging.error(f"Error processing BearerContextSetupRequest: {e}")

    except Exception as e:
        logging.error(f"Error in process_bearer_context_setup_request: {e}")


def process_bearer_context_setup_response(df, item_id, interface):
    try:
        df_filtered = df[df['_ws.col.info'].isin(['BearerContextSetupResponse', 'BearerContextSetupFailure'])]
        with transaction.atomic():
            for index, row in df_filtered.iterrows():
                gnb_cu_cp_ue_e1ap_id = row['e1ap.GNB_CU_CP_UE_E1AP_ID']
                gnb_cu_up_ue_e1ap_id = row['e1ap.GNB_CU_UP_UE_E1AP_ID']
                logging.info(
                    f"E1AP-BearerContextSetupResponse: row: {index}, Message: {row['_ws.col.info']}, gnb_cu_cp_ue_e1ap_id: {gnb_cu_cp_ue_e1ap_id}, gnb_cu_up_ue_e1ap_id:{gnb_cu_up_ue_e1ap_id}")

                if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                    try:
                        existing_identifier = Identifiers.objects.get(
                            GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                            GNB_CU_UP_UE_E1AP_ID__isnull=True,
                            uploadedFiles_id=item_id
                        )

                        existing_identifier.GNB_CU_UP_UE_E1AP_ID = gnb_cu_up_ue_e1ap_id
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)

                    except ObjectDoesNotExist as e:

                        logging.error(f"ObjectDoesNotExist: {e}. Skipping...{row['frame.number']}-{row['_ws.col.info']}")

    except Exception as e:
        logging.error(f"Error in process_bearer_context_setup_response: {e}")


def process_other_e1ap_messages(df, item_id, interface):
    try:
        excluded_messages = ['BearerContextSetupRequest', 'BearerContextSetupResponse', 'BearerContextSetupFailure']
        e1ap_df = df[~df['_ws.col.info'].isin(excluded_messages)]
        with transaction.atomic():
            for index, row in e1ap_df.iterrows():
                gnb_cu_cp_ue_e1ap_id = row['e1ap.GNB_CU_CP_UE_E1AP_ID']
                gnb_cu_up_ue_e1ap_id = row['e1ap.GNB_CU_UP_UE_E1AP_ID']
                logging.info(
                    f"E1AP-Other: row: {index}, Message: {row['_ws.col.info']}, gnb_cu_cp_ue_e1ap_id: {gnb_cu_cp_ue_e1ap_id}, gnb_cu_up_ue_e1ap_id:{gnb_cu_up_ue_e1ap_id}")

                if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                    try:
                        existing_identifier = Identifiers.objects.get(
                            GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                            GNB_CU_UP_UE_E1AP_ID=gnb_cu_up_ue_e1ap_id,
                            uploadedFiles_id=item_id
                        )

                        if existing_identifier:
                            save_messages(row, existing_identifier, interface)

                    except Identifiers.DoesNotExist:

                        logging.warning(f"Identifier does not exist. Skipping...{row['frame.number']}-{row['_ws.col.info']}")

                    except Exception as e:
                        logging.error(f"Error processing other E1AP messages: {e}")

    except Exception as e:
        logging.error(f"Error in process_other_e1ap_messages: {e}")
