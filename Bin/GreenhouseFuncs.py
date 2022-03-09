from os import path
import smtplib
import ssl
import csv
import logging
import datetime
import sys
import json
import shutil
from os.path import exists
from email.message import EmailMessage
from bluetooth import Bulb

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


def c_to_f(temp):
    return (temp * 9/5) + 32


def send_email(subject, message):
    port = 465  # For SSL
    email_config = open_config_dict("EmailConfig.json")
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = email_config["sender"]
    msg['To'] = email_config["receivers"]

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_config["sender"], email_config["sender-pw"])
        server.send_message(msg)

"""
# Used to control a tasmota relay on the local network
def toggle_relay(relay_id, state):
    config_dict = open_config_dict("Config.json")
    ip_address = config_dict["relay_ip"]
    target_url = "http://{}/cm?cmnd=Power{}%20{}".format(ip_address, relay_id, state)
    requests.get(url=target_url)
"""


# Toggles a gpio based on the relay id
def toggle_relay(relay_id, state):
    gpio_dict = {1: 6, 2: 13, 3: 19, 4: 26}
    target_pin = gpio_dict[int(relay_id)]
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(target_pin, GPIO.OUT)
    if state:
        GPIO.output(target_pin, GPIO.LOW)
    else:
        GPIO.output(target_pin, GPIO.HIGH)


# Toggles a gpio pin directly
def toggle_gpio(target_pin, state):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(target_pin, GPIO.OUT)
    if state:
        GPIO.output(target_pin, GPIO.LOW)
    else:
        GPIO.output(target_pin, GPIO.HIGH)


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


def create_logger(name):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # set up the logfile handler
    log_path = path.join(path.dirname(__file__), "../Logs")
    log_filename = path.join(log_path, name + ".log")
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    def my_handler(exc_type, exc_value, exc_traceback):
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

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


def update_config_dict(file_name, data):
    base_path = path.join(path.dirname(path.dirname(__file__)), "Config")
    config_path = path.join(base_path, file_name)

    with open(config_path, "w") as config_file:
        config_file.write(json.dumps(data))


def add_error_flag(flag):
    errors = open_config_dict("Errors.json")

    if flag not in errors["flags"]:
        errors["flags"].append(flag)
        update_config_dict("Errors.json", errors)


def toggle_device(device, toggle):
    config_dict = open_config_dict("Config.json")
    for device_config in config_dict["devices"]:
        if device_config["name"] == device:
            if "direct" == device_config["type"]:
                toggle_gpio(device_config["gpio"], toggle)
            if "bt" in device_config["type"]:
                bulb = Bulb(device_config["mac"])
                bulb.set_power(toggle)


def get_gpio_state(pin):
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        return GPIO.input(pin)
    except NameError:
        return 0


def list_gpio_state():
    gpio_dict = [6,13,19,26]
    for gpio in gpio_dict:
        print("gpio {}: state {}".format(gpio, get_gpio_state(gpio)))
