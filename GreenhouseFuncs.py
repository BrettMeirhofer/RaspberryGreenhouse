import os
import smtplib
import ssl
import requests
import csv
import logging
import datetime


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
    data_file_path = os.path.join(os.path.dirname(__file__), "Data", data_file_path)
    headers = ["Sensor", "Temp", "Humd", "Datetime"]
    if os.path.exists(data_file_path):
        mode = "a"
    else:
        mode = "w"

    data_file = open(data_file_path, mode)
    writer = csv.writer(data_file)

    if not os.path.exists(data_file_path):
        writer.writerow(headers)

    return data_file, writer


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # set up the logfile handler
    log_path = os.path.join(os.path.dirname(__file__), "Logs")
    log_time = datetime.datetime.now()
    log_filename = os.path.join(log_path, "TempHum-%s.log" % log_time.strftime("%Y%m%d-%H%M%S"))
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
