import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn
import GreenhouseFuncs as GHF
from SendData import send_sensor_data
import datetime
import requests
import pytz


# Reads and uploads values from analog sensors
def check_adc():
    logger = GHF.create_logger("CheckADC")
    config_dict = GHF.open_config_dict("Config.json")

    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D7)
    mcp = MCP.MCP3008(spi, cs)
    web_json = {"date": GHF.c_date(), "readings": []}

    for sensor in config_dict["adc_sensors"]:
        sensor = AnalogIn(mcp, getattr(MCP, sensor["port"]))
        web_json["readings"].append({"r": sensor.value, "s": sensor["id"]})

    try:
        send_sensor_data(web_json, "/admin/upload_readings/")
    except requests.exceptions.RequestException:
        logger.error("Upload Failed")


if __name__ == '__main__':
    check_adc()
