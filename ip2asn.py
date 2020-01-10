#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import ipaddress
from logging import getLogger, StreamHandler, DEBUG
# -------------------- Path setting --------------------
# For IPv4
DB_FILE_PATH = './src/ip2asn-v4.tsv'
#
# For IPv6
# DB_FILE_PATH = './ip2asn-v6.tsv'
# ------------------------------------------------------
def create_logger():
    '''Create the logger.
    Args:
    Returns:
        logging.Logger: Representing the logger.
    '''
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
def display_usage():
    '''Display the usage.
    Args:
    Returns:
    '''
    print('[+] Usage:')
    print('        python ip2asn.py [Global IP address]')
    print('    ex. python ip2asn.py 214.0.0.1')
def is_valid_arg_num(argc, valid_arg_num):
    '''Check the number of command line arguments.
    Args:
        argc (int): Representing the number of command line arguments.
        valid_arg_num (int): Representing the correct number of command line arguments.
    Returns:
        bool: Representing the result of checking the number of
              command line arguments.
    '''
    if argc == valid_arg_num:
        return True
    else:
        return False
def load_file(file_path):
    '''Load a file.
    Args:
    Returns:
        list: Repersenting contents of a loaded file.
    '''
    try:
        with open(file_path, 'r') as f:
            return f.readlines()
    except Exception as e:
        logger = create_logger()
        logger.debug(e)
        sys.exit(1)
def convert_str_to_ip(inputted_ip_addr):
    '''Convert str object to IPv4Address object or IPv6Address object.
    Args:
        inputted_ip_addr (str): Representing the inputted IP address of str object.
    Returns:
        ipaddress.IPv4Address or
        ipaddress.IPv6Address: Representing the inputted IP address of
                               IPv4Address object or IPv6Address object.
    '''
    try:
        inputted_ip_addr = ipaddress.ip_address(inputted_ip_addr)
    except Exception as e:
        logger = create_logger()
        logger.debug(e)
        sys.exit(1)
    return inputted_ip_addr
def search_asn(inputted_ip_addr):
    '''Search the correct ASN by Binary Search.
    Args:
        inputted_ip_addr (ipaddress.IPv4Address or
                          ipaddress.IPv6Address): Representing the inputted IP address.
    Returns:
        str: Representing the ASN, AS Description and Country Code.
    '''
    # ----- Load the DB file -----
    ip_db = load_file(DB_FILE_PATH)
    # ----- Initialize the ASN, AS Description and Country Code -----
    as_number = '0'
    as_description = 'N/F'
    country_code = 'N/F'
    # ----- Initialize parameters for Binary Search -----
    low = 0
    high = len(ip_db) - 1
    # ----- Search the correct ASN by Binary Search -----
    while low <= high:
        # ----- Set the middle value -----
        mid = (low + high) // 2
        # ----- Remove '\n' contained in one line of the DB file -----
        replaced_line = ip_db[mid].replace('\n', '')
        # ----- Split one line of the DB file with '\t' -----
        splitted_line = replaced_line.split('\t')
        # ----- Set the start and end of the IP range -----
        range_start = ipaddress.ip_address(splitted_line[0])
        range_end = ipaddress.ip_address(splitted_line[1])
        cidrs = [ipaddr for ipaddr in ipaddress.summarize_address_range(range_start,range_end)]
        # ----- Check if the inputed IP address is within the IP range -----
        if inputted_ip_addr >= range_start and inputted_ip_addr <= range_end:
            as_number = splitted_line[2]
            country_code = splitted_line[3]
            as_description = splitted_line[4]
            break
        else:
            if range_start < inputted_ip_addr and range_end < inputted_ip_addr:
                low = mid + 1
            elif range_start > inputted_ip_addr and range_end > inputted_ip_addr:
                high = mid - 1
    return as_number, as_description, country_code, str(cidrs[0])
def main():
    # ----- Check command line arguments -----
    argvs = sys.argv
    argc = len(argvs)
    if not(is_valid_arg_num(argc, 2)):
        display_usage()
        sys.exit(1)
    # ----- Convert str object to IPv4Address object or IPv6Address object -----
    inputted_ip_addr = convert_str_to_ip(argvs[1])
    # ----- Check if the inputted IP address is a global IP address -----
    if not(inputted_ip_addr.is_global):
        print('\'{0}\' is not a global IP address'.format(inputted_ip_addr))
        sys.exit(1)
    # ----- Search the correct ASN by Binary Search -----
    as_number, as_description, country_code = search_asn(inputted_ip_addr)
    # ----- Display the reuslt of ASN search -----
    print('[+] ASN: {0}'.format(as_number))
    print('[+] AS Description: {0}'.format(as_description))
    print('[+] Country Code: {0}'.format(country_code))
if __name__ == '__main__':
    main()
