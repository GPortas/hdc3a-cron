#!/usr/bin/python3

import sys
import traceback
from datetime import datetime
import logging, re
import os

import requests

DATEFORMAT = '%Y-%m-%d %H:%M:%S'
relative_dir = os.path.dirname(os.path.realpath(__file__))
logname_template = os.path.dirname(os.path.realpath(__file__)) + "/logs/monitor_dropbox_{}.log"
logging.basicConfig(filename=logname_template.format(datetime.today().strftime("%Y%m%d")),
                    format='%(asctime)-2s --%(filename)s-- %(levelname)-8s %(message)s', datefmt=DATEFORMAT,
                    level=logging.DEBUG)

logging.debug("Executing monitor_load_report.py")

def check_dropbox():
    loadreport_files = []
    dropbox_root_dir = os.environ.get('DROPBOX_PATH')
    dropbox_name = os.environ.get('DROPBOX_NAME')
    loadreport_dir = dropbox_root_dir + "/lts_load_reports" + dropbox_name + "/incoming"
    logging.debug("Checking dropbox in " + loadreport_dir)

    for root, dirs, files in os.walk(loadreport_dir):
        for name in files:
            if re.match("LOADREPORT", name):
                loadreport_files.append(name)

    return loadreport_files


def notify_dts(filename):
    dts_endpoint = os.environ.get('DTS_ENDPOINT')
    logging.debug("Calling DTS /loadreport for file: " + filename)
    # Commented out because endpoint doesn't exist yet
    # requests.get(dts_endpoint + '/loadreport?filename=' + filename)


def main():
    loadreport_list = check_dropbox()
    logging.debug("Loadreport files returned: " + str(loadreport_list))
    for loadreport in loadreport_list:
        notify_dts(loadreport)


try:
    main()
    sys.exit(0)
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
