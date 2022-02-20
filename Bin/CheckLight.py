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
    #GPIO.setup(27, GPIO.OUT)
    #GPIO.output(27, GPIO.HIGH)
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D7)
    mcp = MCP.MCP3008(spi, cs)
    print(AnalogIn(mcp, MCP.P2).value)


if __name__ == '__main__':
    check_soil()
