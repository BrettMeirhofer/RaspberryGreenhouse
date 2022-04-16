from os import path
import smtplib
import ssl
import csv
import logging
import datetime
import sys
import json
import shutil
import pytz
from os.path import exists
from email.message import EmailMessage
from helper.bluetooth import Bulb
from helper import esp
from helper import devices

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


# Converts celsius to fahrenheit
def c_to_f(temp):
    return (temp * 9/5) + 32


# Sends an email with the specified title and message
# No longer works with gmail due to increased security requirements
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


# Toggles a gpio pin directly
def toggle_gpio(target_pin, state):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(target_pin, GPIO.OUT)
    if state:
        GPIO.output(target_pin, GPIO.LOW)
    else:
        GPIO.output(target_pin, GPIO.HIGH)


# Creates a logger with the specified name to intercept uncaught errors and write them
def create_logger(name):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # set up the logfile handler
    log_path = path.join(path.dirname(__file__), "../../Logs")
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


# Opens a config json with the specified name and stores it as as a dict
# Copies a default config json into the config dir if file not found
def open_config_dict(file_name):
    base_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "Config")
    config_path = path.join(base_path, file_name)
    if not exists(config_path):
        default_path = path.join(base_path, "Default", "Default" + file_name)
        shutil.copy(default_path, config_path)

    with open(config_path) as config_file:
        config_dict = json.loads(config_file.read())

    return config_dict


# Used for storing persistent data
# Replace with persistent if save data needs expand
def update_config_dict(file_name, data):
    base_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "Config")
    config_path = path.join(base_path, file_name)

    with open(config_path, "w") as config_file:
        json.dump(config_file, data, indent=4, sort_keys=True)


# Error flags indicate the system is currently in an error state and to not send additional emails
def add_error_flag(flag):
    errors = open_config_dict("Errors.json")

    if flag not in errors["flags"]:
        errors["flags"].append(flag)
        update_config_dict("Errors.json", errors)


# Toggle an arbitrary device using a name
def toggle_device(device, toggle):
    config_dict = open_config_dict("Config.json")
    if device in config_dict["devices"]:
        device_config = config_dict["devices"][device]
        toggle_target_device(device_config, toggle, config_dict, device)


# Toggle an arbitrary device using it's config information
def toggle_target_device(device_config, toggle, config_dict, device_name):
    if "direct" == device_config["type"]:
        toggle_gpio(device_config["gpio"], toggle)
    elif "bt" in device_config["type"]:
        bulb = Bulb(device_config["mac"])
        bulb.set_power(toggle)
    elif "esp" in device_config["type"]:
        esp.update_relay(device_config["mac"], device_config["char"], toggle)
        config_dict["devices"][device_name]["state"] = toggle
        update_config_dict("Config.json", config_dict)
    elif "tasmota" in device_config["type"]:
        my_device = devices.TasmotaDevice()
        my_device.ip_address = device_config["ip"]
        my_device.relay_id = device_config["port"]
        my_device.set_state(toggle)


# Gets the state of a physical pin on the board
def get_gpio_state(pin):
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        return not GPIO.input(pin)
    except NameError:
        return 0


# Gets the state of an arbitrary device
def get_device_state(device):
    if device["type"] == "direct":
        return get_gpio_state(device["gpio"])
    elif device["type"] == "esp":
        return device["state"]
    else:
        return "NA"


# Gets the current data in UTC-0
def c_date():
    return datetime.datetime.now(tz=pytz.UTC).strftime("%Y%m%d%H%M")
