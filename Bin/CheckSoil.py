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


def check_soil():
    soil_ids = [5, 6, 7]
    logger = GHF.create_logger("CheckSoil")
    web_json = {"date": datetime.datetime.now(tz=pytz.UTC).strftime("%Y%m%d%H%M"), "readings": []}
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D7)
    mcp = MCP.MCP3008(spi, cs)
    soil_channels = [MCP.P0, MCP.P0, MCP.P0]
    for index, channel in enumerate(soil_channels):
        sensor = AnalogIn(mcp, channel)
        web_json["readings"].append({"r": sensor.value, "s": soil_ids[index]})

    try:
        send_sensor_data(web_json, "/admin/upload_readings/")
    except requests.exceptions.RequestException:
        logger.error("Upload Failed")


if __name__ == '__main__':
    check_soil()
