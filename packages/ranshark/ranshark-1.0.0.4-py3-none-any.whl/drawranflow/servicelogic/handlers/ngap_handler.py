import logging
import pandas as pd
from django.db import transaction
from drawranflow.models import Identifiers, Message
from .utils import save_messages


def process_ngap_dataframe(df, item_id, interface):
    try:
        ngap_df = df[df['frame.protocols'].str.lower().str.contains('ngap', na=False, regex=False)]
        ngap_df['ngap.RAN_UE_NGAP_ID'] = ngap_df['ngap.RAN_UE_NGAP_ID'].astype(str)

        with transaction.atomic():
            ngap_df.groupby('ngap.RAN_UE_NGAP_ID').apply(
                lambda group_df: process_ngap_group(group_df, item_id, interface)
            )

    except Exception as e:
        logging.error(f"Error processing ngap dataframe: {e}")


def process_ngap_group(group_df, item_id, interface):
    try:
        logging.debug(f"Processing NGAP messages for RAN_UE_NGAP_ID: {group_df['ngap.RAN_UE_NGAP_ID'].iloc[0]}")
        process_ngap_service_request(group_df, item_id, interface)
        process_ngap_initial_context_messages(group_df, item_id, interface)
        process_ngap_other_messages(group_df, item_id, interface)

    except Exception as e:
        logging.error(f"Error processing group: {e}")


def process_ngap_service_request(df, item_id, interface):
    try:
        included_messages = ["Service request", "Registration request", "Tracking area update request"]
        ngap_df = df[df['_ws.col.info'].isin(included_messages)]

        with transaction.atomic():
            valid_rows = ~ngap_df['ngap.RAN_UE_NGAP_ID'].isnull() & ngap_df['ngap.AMF_UE_NGAP_ID'].isnull()
            valid_ngap_ids = ngap_df.loc[valid_rows, 'ngap.RAN_UE_NGAP_ID'].astype(str).tolist()

            identifiers_filter = {
                'GNB_CU_UE_F1AP_ID__in': valid_ngap_ids,
                'RAN_UE_NGAP_ID__isnull': True,
                'AMF_UE_NGAP_ID__isnull': True,
                'uploadedFiles_id': item_id
            }

            existing_identifiers = Identifiers.objects.filter(**identifiers_filter)

            for _, row in ngap_df[valid_rows].iterrows():
                try:
                    existing_identifier = existing_identifiers.get(
                        GNB_CU_UE_F1AP_ID=row['ngap.RAN_UE_NGAP_ID'],
                        RAN_UE_NGAP_ID__isnull=True,
                        AMF_UE_NGAP_ID__isnull=True,
                        uploadedFiles_id=item_id
                    )

                    if row['_ws.col.info'] in included_messages:
                        rrc_setup_complete_exists = Message.objects.filter(
                            identifiers_id=existing_identifier.id,
                            Message__iexact='Service request'.strip(),
                            Protocol__icontains='f1ap'
                        ).exists()
                        reg_complete_exists = Message.objects.filter(
                            identifiers_id=existing_identifier.id,
                            Message__iexact='Registration request'.strip(),
                            Protocol__icontains='f1ap'
                        ).exists()
                        track_complete_exists = Message.objects.filter(
                            identifiers_id=existing_identifier.id,
                            Message__iexact='Tracking area update request'.strip(),
                            Protocol__icontains='f1ap'
                        ).exists()

                        logging.info(
                            f"NGAP-process_ngap_service_request Message: {row['_ws.col.info']}, "
                            f"frameNumber: {row['frame.number']}, "
                            f"rrc_setup_complete_exists: {rrc_setup_complete_exists}, "
                            f"reg_complete_exists: {reg_complete_exists}, "
                            f"track_complete_exists: {track_complete_exists}")

                        if rrc_setup_complete_exists or reg_complete_exists or track_complete_exists:
                            existing_identifier.RAN_UE_NGAP_ID = row['ngap.RAN_UE_NGAP_ID']
                            existing_identifier.save()
                            save_messages(row, existing_identifier, interface)

                except Identifiers.DoesNotExist:
                    logging.warning("Identifier does not exist. Skipping...")

    except Exception as e:
        logging.error(f"Error processing NGAP messages: {e}")


def process_ngap_initial_context_messages(df, item_id, interface):
    try:
        initial_context_df = df[
            df['_ws.col.info'].str.contains('InitialContextSetupRequest|Registration reject', case=False, na=False)
        ]

        with transaction.atomic():
            valid_rows = ~initial_context_df['ngap.RAN_UE_NGAP_ID'].isnull() & ~initial_context_df[
                'ngap.AMF_UE_NGAP_ID'].isnull()
            valid_ran_ue_ngap_ids = initial_context_df.loc[valid_rows, 'ngap.RAN_UE_NGAP_ID'].astype(str).tolist()
            valid_amf_ue_ngap_ids = initial_context_df.loc[valid_rows, 'ngap.AMF_UE_NGAP_ID'].astype(str).tolist()

            identifiers_filter = {
                'RAN_UE_NGAP_ID__in': valid_ran_ue_ngap_ids,
                'AMF_UE_NGAP_ID__isnull': True,
                'uploadedFiles_id': item_id
            }

            existing_identifiers = Identifiers.objects.filter(**identifiers_filter)

            for _, row in initial_context_df[valid_rows].iterrows():
                try:
                    existing_identifier = existing_identifiers.get(
                        RAN_UE_NGAP_ID=row['ngap.RAN_UE_NGAP_ID']
                    )

                    if existing_identifier:
                        if not pd.isnull(row['ngap.AMF_UE_NGAP_ID']):
                            existing_identifier.AMF_UE_NGAP_ID = row['ngap.AMF_UE_NGAP_ID']
                            existing_identifier.save()
                            save_messages(row, existing_identifier, interface)

                except Identifiers.DoesNotExist:
                    logging.warning(f"Identifier does not exist. Skipping...{row['frame.number']}-{row['_ws.col.info']}")

    except Exception as e:
        logging.error(f"Error processing NGAP InitialContextSetupRequest/Registration reject messages: {e}")


def process_ngap_other_messages(df, item_id, interface):
    try:
        excluded_messages = ["Service request", "Registration request", "Tracking area update request"]
        other_ngap_df = df[~df['_ws.col.info'].isin(excluded_messages)]

        with transaction.atomic():
            valid_rows = ~other_ngap_df['ngap.RAN_UE_NGAP_ID'].isnull() & ~other_ngap_df['ngap.AMF_UE_NGAP_ID'].isnull()
            valid_ran_ue_ngap_ids = other_ngap_df.loc[valid_rows, 'ngap.RAN_UE_NGAP_ID'].astype(str).tolist()
            valid_amf_ue_ngap_ids = other_ngap_df.loc[valid_rows, 'ngap.AMF_UE_NGAP_ID'].astype(str).tolist()

            identifiers_filter = {
                'RAN_UE_NGAP_ID__in': valid_ran_ue_ngap_ids,
                'AMF_UE_NGAP_ID__in': valid_amf_ue_ngap_ids,
                'uploadedFiles_id': item_id
            }

            existing_identifiers = Identifiers.objects.filter(**identifiers_filter)

            for _, row in other_ngap_df[valid_rows].iterrows():
                try:
                    existing_identifier = existing_identifiers.get(
                        RAN_UE_NGAP_ID=row['ngap.RAN_UE_NGAP_ID']
                    )

                    if existing_identifier:
                        registration_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Registration request',
                            Protocol__icontains='ngap'
                        ).exists()
                        service_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Service request',
                            Protocol__icontains='ngap'
                        ).exists()
                        tracking_area_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Tracking area update request',
                            Protocol__icontains='ngap'
                        ).exists()

                        logging.debug(
                            f" message: {row['_ws.col.info']}, "
                            f"registration_exists {registration_exists}, "
                            f"registration_exists {service_exists}, "
                            f"registration_exists {tracking_area_exists}")

                        if registration_exists or service_exists or tracking_area_exists:
                            save_messages(row, existing_identifier, interface)
                        else:
                            logging.debug(
                                f"Skipping DB update/inserts for row {index}, "
                                f"Registration request/Service request/Tracking area not found "
                                f"in Messages for the identifier.")

                except Identifiers.DoesNotExist:
                    logging.error(f"process_ngap_other_messages- Identifier does not exist. Skipping..."
                                  f"row: {row['frame.number']}, Message {row['_ws.col.info']}, Ran id: {row['ngap.RAN_UE_NGAP_ID']}")

    except Exception as e:
        logging.error(f"Error processing other NGAP messages: {e}")
