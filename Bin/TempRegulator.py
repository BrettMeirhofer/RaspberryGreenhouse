import datetime
import GreenhouseFuncs as GHF
from SendData import send_sensor_data
import requests
import json
import pytz
import sys


# Microcontroller exclusive libraries that break testing on pc
try:
    import RPi.GPIO as GPIO
    import board
    import adafruit_ahtx0
    import adafruit_tca9548a
except ImportError:
    pass


# Maintains greenhouse temperature by toggling a heater on a Tasmota relay based on temperature reported from sensors
# Sends heater status and sensor data to a remote web server for ingesting into a database
def handle_temp():
    config_dict = GHF.open_config_dict("Config.json")
    logger = GHF.create_logger("TempRegulator")
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    i2c = board.I2C()  # uses board.SCL and board.SDA
    tca = adafruit_tca9548a.TCA9548A(i2c)

    temps = []
    current_date = datetime.datetime.now(tz=pytz.UTC).strftime("%Y%m%d%H%M")
    temp_json = {"date": current_date, "readings": []}

    for sensor_config in config_dict["temp_sensors"]:
        sensor = adafruit_ahtx0.AHTx0(tca[sensor_config["port"]])
        sensor_temp = round(sensor.temperature, 1)
        sensor_humd = round(sensor.relative_humidity, 1)
        temp_json["readings"].append({"r": sensor_temp, "s": sensor_config["temp_id"]})
        temp_json["readings"].append({"r": sensor_humd, "s": sensor_config["humd_id"]})
        temps.append(sensor_temp)

    enable_heater = temps[0] < config_dict["heater_temp"]

    GPIO.cleanup()

    send_temp_data(logger, temp_json)

    if config_dict["heating"]:
        heater_json = {"device": 1, "status": int(enable_heater), "date": current_date}
        send_heater_status(logger, heater_json)
        toggle_heater(logger, config_dict, enable_heater)

    temp_errors(temps[0], config_dict, temp_json)


# Informs remote if heater is on/off
def send_heater_status(logger, heater_json):
    try:
        send_sensor_data(heater_json, "/admin/Device/")
    except requests.exceptions.RequestException:
        logger.error("Heater Status Upload Failed")


# Physically controls the on/off state of heater
def toggle_heater(logger, config_dict, enable_heater):
    try:
        GHF.toggle_relay(config_dict["heater_relay"], enable_heater)
    except requests.exceptions.RequestException:
        logger.error("Relay Control Failed")


# Sends temp/humd to remote every 30 mins or if triggered by cmd
def send_temp_data(logger, temp_json):
    try:
        cmd_line = sys.argv[1] == "f"
    except IndexError:
        cmd_line = False

    if datetime.datetime.now().minute % 30 == 0 or cmd_line:
        try:
            send_sensor_data(temp_json, "/admin/upload_readings/")
            send_sensor_data({}, "/admin/Temp/")
        except requests.exceptions.RequestException:
            logger.error("TempRegulator Data Upload Failed")


def temp_errors(temp, config_dict, logger):
    errors = GHF.open_config_dict("Errors.json")
    temp_f = GHF.c_to_f(temp)

    if temp > config_dict["too_hot"] and ("too_hot" not in errors["flags"]):
        if logger is not None:
            logger.error("Greenhouse Overheating")
        GHF.send_email("Greenhouse Too Hot", "You are being notified because the greenhouse "
                                             "temperature {}F is higher than the maximum temp {}F."
                       .format(temp_f, GHF.c_to_f(config_dict["too_hot"])))
        GHF.add_error_flag("too_hot")

    if temp < config_dict["too_cold"] and ("too_cold" not in errors["flags"]):
        if logger is not None:
            logger.error("Greenhouse Too Cold")
        GHF.send_email("Greenhouse Too Cold", "You are being notified because the greenhouse "
                                              "temperature {}F is lower than the minimum temp {}F."
                       .format(temp_f, GHF.c_to_f(config_dict["too_cold"])))
        GHF.add_error_flag("too_cold")


if __name__ == '__main__':
    handle_temp()

# Add Hot/Cold Emails
# Add Data emails
