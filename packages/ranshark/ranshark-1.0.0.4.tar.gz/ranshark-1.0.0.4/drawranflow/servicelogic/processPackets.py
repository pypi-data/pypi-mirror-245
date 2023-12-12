import os
import subprocess
import json
import datetime
import time

import pandas as pd
from .handlers import f1ap_handler as fh
from drawranflow.models import UploadedFile
from django.utils import timezone
import math
import numpy as np

def extract_last_info(row):
    if "Not used in current version" in row:
        print(f"{row}")
        parts = row.split(', Not')[0]
        print(parts)
        row = parts
    parts = row.split(', ')
    for part in reversed(parts):

       
        if 'MAC=' in part:
            return part.split('MAC=')[0].rstrip()
        if '[' in part:
            return part.split('[')[0].strip()
        if '(' in part:
            return part.split('(')[0].strip()

        
        return part.rstrip()

# Function to split values and store in separate columns
def split_values(row):
    row = str(row)
    row = row.strip()
    if pd.notna(row) or not str(row).lower() != 'nan':
        values = str(row).split(',')
        return values[0] if len(values) >0 else np.nan, values[1] if len(values) >1 else np.nan
    else:
        return pd.Series([np.nan ,np.nan])

class F1APHandlerE:
    def __init__(self, input_pcap, output_csv, item_id):
        self.input_pcap = input_pcap
        self.output_csv = output_csv
        self.item_id = item_id

    def capture_packets_and_save_to_csv(self):
        try:
            filtered_file = f'{self.input_pcap}_filtered'
            tshark_c = ['tshark', '-r', self.input_pcap, '-Y', 'f1ap||e1ap||ngap||xnap', '-w', filtered_file]

            # Define the tshark command
            result = subprocess.run(tshark_c, stdout=subprocess.PIPE, text=True, check=True)
            os.replace(filtered_file, self.input_pcap)

            if result:
                tshark_command = [
                    'tshark', '-r', self.input_pcap, '-T', 'fields',
                    '-e', 'frame.number',
                    '-e', 'frame.time',
                    '-e', 'ip.src',
                    '-e', 'ip.dst',
                    '-e', 'frame.protocols',
                    '-e', 'f1ap.C_RNTI',
                    '-e', 'f1ap.GNB_DU_UE_F1AP_ID',
                    '-e', 'f1ap.GNB_CU_UE_F1AP_ID',
                    '-e', 'e1ap.GNB_CU_CP_UE_E1AP_ID',
                    '-e', 'e1ap.GNB_CU_UP_UE_E1AP_ID',
                    '-e', 'ngap.RAN_UE_NGAP_ID',
                    '-e', 'ngap.AMF_UE_NGAP_ID',
                    '-e', 'f1ap.procedureCode',
                    '-e', 'e1ap.procedureCode',
                    '-e', 'ngap.procedureCode',
                    '-e', 'nr-rrc.c1',
                    '-e', 'nr-rrc.c2',
                    '-e', 'nr-rrc.pdcch_DMRS_ScramblingID',
                    '-e', 'nas_5gs.sm.message_type',
                    '-e', 'nas_5gs.mm.message_type',
                    '-e', '_ws.col.Info',
                    '-e', 'xnap.NG_RANnodeUEXnAPID',
                    '-E', 'header=y',
                    '-E', 'separator=;',
                    '-Y', 'f1ap||e1ap||ngap||xnap'
                ]

                # Run tshark and capture the output
                result = subprocess.run(tshark_command, stdout=subprocess.PIPE, text=True, check=True)

                # Save the CSV data to the output file
                with open(self.output_csv, 'w') as csv_file:
                    csv_created = csv_file.write(result.stdout)
                upload_file = UploadedFile.objects.get(id=self.item_id)
                # logging.debug(f"Tshark successfully filterd and csv created , {result}, {csv_created}")

                if result and csv_created:
                    setattr(upload_file, 'proces_date', timezone.now())
                    setattr(upload_file, 'processed', True)
                upload_file.save()
                print(f"Data saved to {self.output_csv}")

        except subprocess.CalledProcessError as e:
             logging.error(f"Error running tshark: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        dtypes = {
            'frame.number': str,
            'frame.time': str,
            'ip.src': str,
            'ip.dst': str,
            'frame.protocols': str,
            'f1ap.C_RNTI': str,
            'f1ap.GNB_DU_UE_F1AP_ID': str,
            'f1ap.GNB_CU_UE_F1AP_ID': str,
            'e1ap.GNB_CU_CP_UE_E1AP_ID': str,
            'e1ap.GNB_CU_UP_UE_E1AP_ID': str,
            'ngap.RAN_UE_NGAP_ID': str,
            'ngap.AMF_UE_NGAP_ID': str,
            'f1ap.procedureCode': str,
            'e1ap.procedureCode': str,
            'ngap.procedureCode': str,
            'nr-rrc.c1': str,
            'nr-rrc.c2': str,
            'nr-rrc.pdcch_DMRS_ScramblingID': str,
            'nas_5gs.sm.message_type': str,
            'nas_5gs.mm.message_type': str,
            '_ws.col.Info': str,
            'xnap.NG_RANnodeUEXnAPID': str,
        }
        
        df = pd.read_csv(self.output_csv, sep=';', dtype=dtypes, parse_dates=['frame.time'])

        df['_ws.col.info'] = df['_ws.col.Info'].apply(extract_last_info)

        df = df.rename(columns={"nas_5gs.sm.message_type" : "nas-5gs.sm.message_type", "nas_5gs.mm.message_type" : "nas-5gs.mm.message_type", "nr-rrc.pdcch_DMRS_ScramblingID" : "nr-rrc.pdcch-DMRS-ScramblingID"})
        # df['xnap.NG_RANnodeUEXnAPID_src'] = df['xnap.NG_RANnodeUEXnAPID'].str.split(',', expand=True)[0]
        # df['xnap.NG_RANnodeUEXnAPID_dst'] = df['xnap.NG_RANnodeUEXnAPID'].str.split(',', expand=True)[1]

        df[['xnap.NG_RANnodeUEXnAPID_src', 'xnap.NG_RANnodeUEXnAPID_dst']] = df['xnap.NG_RANnodeUEXnAPID'].apply(lambda x: pd.Series(split_values(x)))
        # Drop the original 'NG_RANnodeUEXnAPID and _ws.col.Info' column
        df = df.drop('xnap.NG_RANnodeUEXnAPID', axis=1)
        df = df.drop('_ws.col.Info', axis=1)
        
        for index, row in df.iterrows():
            proto = row['frame.protocols'].split(':')

            if "f1ap" in proto:
                try:
                    fh.process_dataframe(row, index, 'f1ap', self.item_id)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

            if "e1ap" in proto:
                try:
                    fh.process_e1dataframe(row, index, 'e1ap',self.item_id)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

            if "ngap" in proto:
                try:
                    fh.process_ngapdataframe(row, index, 'ngap',self.item_id)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

            if "xnap" in proto:
                try:
                    fh.process_xnapdataframe(row, index, 'xnap',self.item_id)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

        setattr(upload_file, 'complete_at', timezone.now())
        setattr(upload_file, 'completed', True)
        upload_file.save()
