from os import path
import smtplib
import ssl
import requests
import csv
import logging
import datetime
import sys
import json
import shutil
from os.path import exists


def send_email(message, sender, sender_pw, receivers):
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, sender_pw)
        for receiver in receivers:
            server.sendmail(sender, receiver, message)


# Used to control a tasmota relay on the local network
def toggle_relay(relay_id, state):
    ip_address = "192.168.1.179"
    target_url = "http://{}/cm?cmnd=Power{}%20{}".format(ip_address, relay_id, state)
    requests.get(url=target_url)


def get_data_file(file_name):
    data_file_path = file_name + datetime.datetime.now().strftime("%Y%m%d") + ".csv"
    data_file_path = path.join(path.dirname(__file__), "../Data", data_file_path)
    headers = ["Sensor", "Temp", "Humd", "Datetime"]
    if path.exists(data_file_path):
        mode = "a"
    else:
        mode = "w"

    data_file = open(data_file_path, mode)
    writer = csv.writer(data_file)

    if not path.exists(data_file_path):
        writer.writerow(headers)

    return data_file, writer


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # set up the logfile handler
    log_path = path.join(path.dirname(__file__), "../Logs")
    log_time = datetime.datetime.now()
    log_filename = path.join(log_path, "TempHum-%s.log" % log_time.strftime("%Y%m%d-%H%M%S"))
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    def my_handler(type, value, tb):
        logger.exception("Uncaught exception: {0}".format(str(value)))

    # Install exception handler
    sys.excepthook = my_handler
    return logger


def open_config_dict(file_name):
    base_path = path.join(path.dirname(path.dirname(__file__)), "Config")
    config_path = path.join(base_path, file_name)
    if not exists(config_path):
        default_path = path.join(base_path, "Default", "Default" + file_name)
        shutil.copy(default_path, config_path)

    with open(config_path) as config_file:
        config_dict = json.loads(config_file.read())

    return config_dict
