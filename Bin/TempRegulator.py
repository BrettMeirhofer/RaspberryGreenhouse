import board
import adafruit_ahtx0
import adafruit_tca9548a
import datetime
import GreenhouseFuncs as GHF
from SendData import send_sensor_data
import RPi.GPIO as GPIO
import requests
import json


# Maintains greenhouse temperature by toggling a heater on a Tasmota relay based on temperature reported from sensors
# Sends heater status and sensor data to a remote web server for ingesting into a database
def handle_temp():
    config_dict = GHF.open_config_dict("Config.json")
    logger = GHF.create_logger("TempRegulator")
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    i2c = board.I2C()  # uses board.SCL and board.SDA
    tca = adafruit_tca9548a.TCA9548A(i2c)
    multi_ports = [1, 2]

    temps = []
    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    temp_json = {"date": current_date, "readings": []}

    for index, port in enumerate(multi_ports):
        sensor = adafruit_ahtx0.AHTx0(tca[port])
        sensor_temp = round(sensor.temperature, 1)
        sensor_humd = round(sensor.relative_humidity, 1)
        temp_json["readings"].extend([sensor_temp, sensor_humd])
        temps.append(sensor_temp)

    enable_heater = temps[0] < config_dict["heater_temp"]
    GPIO.cleanup()

    if datetime.datetime.now().minute == 30:
        try:
            send_sensor_data(temp_json, "/admin/Temp/")
        except requests.exceptions.RequestException:
            logger.error("TempRegulator Data Upload Failed")

    heater_json = {"device": 1, "status": int(enable_heater), "date": current_date}

    try:
        send_sensor_data(heater_json, "/admin/Device/")
    except requests.exceptions.RequestException:
        logger.error("Heater Status Upload Failed")

    try:
        GHF.toggle_relay(1, enable_heater)
    except requests.exceptions.RequestException:
        logger.error("Relay Control Failed")

    # Need a way to remember errors to prevent email spamming
    """
    if avg_temp > config_dict["too_hot"]:
        logger.error("Greenhouse Overheating")
        send_email("Greenhouse Overheating")

    if avg_temp < config_dict["too_cold"]:
        logger.error("Greenhouse Too Cold")
        send_email("Greenhouse Too Cold")
    """


if __name__ == '__main__':
    handle_temp()

# Add Hot/Cold Emails
# Add Data emails
