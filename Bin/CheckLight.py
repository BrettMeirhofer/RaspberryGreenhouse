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


def check_light():
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D7)
    mcp = MCP.MCP3008(spi, cs)
    readings = []
    for x in range(9):
        readings.append(AnalogIn(mcp, MCP.P2).value)
        time.sleep(.5)
    readings.sort()
    print(readings)


if __name__ == '__main__':
    check_light()
