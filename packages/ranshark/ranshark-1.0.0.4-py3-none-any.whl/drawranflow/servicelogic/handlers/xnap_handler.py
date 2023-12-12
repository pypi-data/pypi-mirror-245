import logging
import pandas as pd
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from drawranflow.models import Identifiers, Message
from .utils import save_messages


def process_xnap_dataframe(df, item_id, interface):
    try:
        xnap_df = df[df['frame.protocols'].apply(lambda x: 'xnap' in x.lower() if isinstance(x, str) else False)]
        xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_src'] = pd.to_numeric(xnap_df['xnap.NG_RANnodeUEXnAPID_src'],
                                                                      errors='coerce')
        xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_dst'] = pd.to_numeric(xnap_df['xnap.NG_RANnodeUEXnAPID_dst'],
                                                                      errors='coerce')

        grouped_df = xnap_df.groupby(['xnap.NG_RANnodeUEXnAPID_src'])
        with transaction.atomic():
            for _, group_df in grouped_df:
                try:
                    logging.debug(
                        f"Processing XNAP messages for NG_RANnodeUEXnAPID_src: {group_df['xnap.NG_RANnodeUEXnAPID_src'].iloc[0]}")
                    process_xnap_handover_request(group_df, item_id, interface)
                    process_xnap_handover_acknowledge(group_df, item_id, interface)
                    process_xnap_other_messages(group_df, item_id, interface)
                except Exception as e:
                    logging.error(f"Error processing group: {e}")
    except Exception as e:
        logging.error(f"Error processing xnap dataframe: {e}")


def process_xnap_handover_request(df, item_id, interface):
    try:
        included_messages = ["HandoverRequest"]
        xnap_df = df[df['_ws.col.info'].isin(included_messages)]
        with transaction.atomic():
            if not xnap_df.empty:
                xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_src'] = pd.to_numeric(xnap_df['xnap.NG_RANnodeUEXnAPID_src'],
                                                                              errors='coerce')
                xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_dst'] = pd.to_numeric(xnap_df['xnap.NG_RANnodeUEXnAPID_dst'],
                                                                              errors='coerce')

                src_ran_ids = xnap_df['xnap.NG_RANnodeUEXnAPID_src']
                trg_ran_ids = xnap_df['xnap.NG_RANnodeUEXnAPID_dst']

                valid_rows = ~src_ran_ids.isnull() & trg_ran_ids.isnull()
                valid_src_ran_ids = src_ran_ids[valid_rows].astype(str).tolist()
                identifiers_filter = {
                    'GNB_CU_UE_F1AP_ID__in': valid_src_ran_ids,
                    'XNAP_SRC_RAN_ID__isnull': True,
                    'XNAP_TRGT_RAN_ID__isnull': True,
                    'AMF_UE_NGAP_ID__isnull': False,
                    'uploadedFiles_id': item_id
                }
                existing_identifiers = Identifiers.objects.filter(**identifiers_filter)
                for _, row in xnap_df[valid_rows].iterrows():
                    try:
                        existing_identifier = existing_identifiers.get(
                            GNB_CU_UE_F1AP_ID=row['xnap.NG_RANnodeUEXnAPID_src'],
                            XNAP_SRC_RAN_ID__isnull=True,
                            XNAP_TRGT_RAN_ID__isnull=True,
                            AMF_UE_NGAP_ID__isnull=False,
                            uploadedFiles_id=item_id
                        )
                        if row['_ws.col.info'] in included_messages:
                            rrc_setup_complete_exists = Message.objects.filter(
                                identifiers_id=existing_identifier.id,
                                Message__iexact='Service request'.strip()
                            ).exists()
                            reg_complete_exists = Message.objects.filter(
                                identifiers_id=existing_identifier.id,
                                Message__iexact='Registration request'.strip()
                            ).exists()
                            track_complete_exists = Message.objects.filter(
                                identifiers_id=existing_identifier.id,
                                Message__iexact='Tracking area update request'.strip()
                            ).exists()
                            if rrc_setup_complete_exists or reg_complete_exists or track_complete_exists:
                                existing_identifier.XNAP_SRC_RAN_ID = row['xnap.NG_RANnodeUEXnAPID_src']
                                existing_identifier.save()
                                save_messages(row, existing_identifier, interface)

                    except Identifiers.DoesNotExist:
                        logging.warning("Identifier does not exist. Skipping...")
                        continue

    except Exception as e:
        logging.error(f"Error processing XNAP HandoverRequest messages: {e}")


def process_xnap_handover_acknowledge(df, item_id, interface):
    try:
        acknowledge_df = df[df['_ws.col.info'].str.contains('HandoverRequestAcknowledge', case=False, na=False)]

        with transaction.atomic():
            if not acknowledge_df.empty:
                acknowledge_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_src'] = pd.to_numeric(
                    acknowledge_df['xnap.NG_RANnodeUEXnAPID_src'], errors='coerce'
                )

                acknowledge_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_dst'] = pd.to_numeric(
                    acknowledge_df['xnap.NG_RANnodeUEXnAPID_dst'], errors='coerce'
                )

                src_ran_ids = acknowledge_df['xnap.NG_RANnodeUEXnAPID_src']
                trg_ran_ids = acknowledge_df['xnap.NG_RANnodeUEXnAPID_dst']

                valid_rows = ~src_ran_ids.isnull() & ~trg_ran_ids.isnull()
                valid_src_ran_ids = src_ran_ids[valid_rows].astype(str).tolist()
                valid_trg_ran_ids = trg_ran_ids[valid_rows].astype(str).tolist()

                identifiers_filter = {
                    'XNAP_SRC_RAN_ID__in': valid_src_ran_ids,
                    'RAN_UE_NGAP_ID__in': valid_src_ran_ids,
                    'XNAP_TRGT_RAN_ID__isnull': True,
                    'uploadedFiles_id': item_id
                }

                existing_identifiers = Identifiers.objects.filter(**identifiers_filter)

                for _, row in acknowledge_df[valid_rows].iterrows():
                    try:
                        existing_identifier = existing_identifiers.get(
                            XNAP_SRC_RAN_ID=row['xnap.NG_RANnodeUEXnAPID_src'],
                            RAN_UE_NGAP_ID=row['xnap.NG_RANnodeUEXnAPID_src'],
                            XNAP_TRGT_RAN_ID__isnull=True,
                            uploadedFiles_id=item_id
                        )
                        if existing_identifier:
                            existing_identifier.XNAP_TRGT_RAN_ID = row['xnap.NG_RANnodeUEXnAPID_dst']
                            existing_identifier.save()
                            save_messages(row, existing_identifier, interface)

                    except ObjectDoesNotExist as e:
                        logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                        pass

    except Exception as e:
        logging.error(f"Error processing XNAP HandoverRequestAcknowledge messages: {e}")


def process_xnap_other_messages(df, item_id, interface):
    try:
        excluded_messages = ["HandoverRequest"]
        other_xnap_df = df[~df['_ws.col.info'].isin(excluded_messages)]

        with transaction.atomic():
            if not other_xnap_df.empty:
                other_xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_src'] = pd.to_numeric(
                    other_xnap_df['xnap.NG_RANnodeUEXnAPID_src'], errors='coerce')
                other_xnap_df.loc[:, 'xnap.NG_RANnodeUEXnAPID_dst'] = pd.to_numeric(
                    other_xnap_df['xnap.NG_RANnodeUEXnAPID_dst'], errors='coerce')

                src_ran_ids = other_xnap_df['xnap.NG_RANnodeUEXnAPID_src']
                trg_ran_ids = other_xnap_df['xnap.NG_RANnodeUEXnAPID_dst']

                valid_rows = ~src_ran_ids.isnull() & ~trg_ran_ids.isnull()
                valid_src_ran_ids = src_ran_ids[valid_rows].astype(str).tolist()
                valid_trg_ran_ids = trg_ran_ids[valid_rows].astype(str).tolist()

                identifiers_filter = {
                    'XNAP_SRC_RAN_ID__in': valid_src_ran_ids,
                    'XNAP_TRGT_RAN_ID__in': valid_trg_ran_ids,
                    'uploadedFiles_id': item_id
                }

                existing_identifiers = Identifiers.objects.filter(**identifiers_filter)

                for _, row in other_xnap_df[valid_rows].iterrows():
                    try:
                        existing_identifier = existing_identifiers.get(
                            XNAP_SRC_RAN_ID=row['xnap.NG_RANnodeUEXnAPID_src'],
                            XNAP_TRGT_RAN_ID=row['xnap.NG_RANnodeUEXnAPID_dst'],
                            uploadedFiles_id=item_id
                        )
                        if existing_identifier:
                            save_messages(row, existing_identifier, interface)

                    except ObjectDoesNotExist as e:
                        logging.warning("Identifier does not exist. Skipping...")

    except Exception as e:
        logging.error(f"Error processing other XNAP messages: {e}")
