import logging
from django.conf import settings
import os
import json
import pandas as pd
import numpy as np
from drawranflow.models import Message, Identifiers, UploadedFile
from django.db import IntegrityError
import logging


def decimal_to_binary(n):
    return bin(n).replace("0b", "")


def binary_to_decimal(b):
    return int(b, 2)


def hex_to_decimal(h):
    if pd.notna(h) and h.lower() != 'nan':
        try:
            return int(h.replace(":", ""), 16)
        except ValueError as e:
            logging.error(f"Error in gid function: {e}")
    return np.nan


def extract_bits(binary, num_bits):
    return binary[:num_bits]


def get_gnb_id(h):
    try:
        # Check if h is an integer, and if so, convert it to a hexadecimal string
        if isinstance(h, int):
            h = hex(h)
        # Assuming these functions are available in your codebase
        decimal_num = hex_to_decimal(h)
        logging.debug(f"Decimal representation of {h}: {decimal_num}")

        binary_num = decimal_to_binary(decimal_num)
        logging.debug(f"Binary representation of {decimal_num}: {binary_num}")

        # Extract first 19 bits
        extracted_bits = extract_bits(binary_num, 19)
        logging.debug(f"Extracted 19 bits from {binary_num}: {extracted_bits}")

        # Convert extracted bits back to decimal
        decimal_again = binary_to_decimal(extracted_bits)
        logging.debug(f"Decimal representation of extracted bits {extracted_bits}: {decimal_again}")

        return str(decimal_again)
    except Exception as e:
        logging.error(f"Error in gid function: {e}")
        return "Error"


def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File Not found {file_name}"
    return data


def configure_logging(log_file_path):
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d]- %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
        ]
    )


# Configuration for log file path
BASE_DIR = getattr(settings, 'BASE_DIR', None)
LOG_FILE_PATH = os.path.join(BASE_DIR, 'debug.log')
configure_logging(LOG_FILE_PATH)

INTERFACE_CONFIG = {}


def load_interface_config(interfaces):
    global INTERFACE_CONFIG
    for interface in interfaces:
        direction = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'intfconfig', f'{interface}_proc.json'))
        INTERFACE_CONFIG[interface] = open_file(direction)


load_interface_config(['f1ap', 'e1ap', 'ngap', 'xnap'])


def load_cause_config(interface):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'intfconfig', f'{interface}_cause.json'))
    with open(file_path, 'r') as file:
        cause_json = json.load(file)

    cause_df = pd.DataFrame(cause_json)

    return cause_df


def get_direction(message, interface):
    if isinstance(message, list):
        message = message[0]

    directions = INTERFACE_CONFIG.get(interface)

    if directions is None:
        logging.warning(f'INTERFACE_CONFIG not found for interface: {interface}')
        return None, None

    for key, values in directions.items():
        if key.lower() == message.lower():
            directions = values

    src_node = directions.get("srcNode")
    dst_node = directions.get("dstNode")
    if src_node is None:
        logging.error(f' message is not found in  {interface}, message {message}')

    return src_node, dst_node


def get_interface_from_protocol(protocol):
    if "f1ap" in protocol.lower():
        return "f1ap"
    elif "ngap" in protocol.lower():
        return "ngap"
    elif "e1ap" in protocol.lower():
        return "e1ap"
    elif "xnap" in protocol.lower():
        return "xnap"
    else:
        return "unknown"


