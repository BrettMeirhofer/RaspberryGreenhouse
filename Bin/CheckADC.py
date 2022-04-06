import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from Bin.helper import GreenhouseFuncs as GHF
from Bin.helper.SendData import send_sensor_data
import requests


# Reads and uploads values from analog sensors
def check_adc():
    logger = GHF.create_logger("CheckADC")
    config_dict = GHF.open_config_dict("Config.json")

    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D7)
    mcp = MCP.MCP3008(spi, cs)
    web_json = {"date": GHF.c_date(), "readings": []}

    for sensor_config in config_dict["adc_sensors"]:
        sensor = AnalogIn(mcp, getattr(MCP, sensor_config["port"]))
        web_json["readings"].append({"r": sensor.value, "s": sensor_config["id"]})

    try:
        send_sensor_data(web_json, "/admin/upload_readings/")
    except requests.exceptions.RequestException:
        logger.error("Upload Failed")


if __name__ == '__main__':
    check_adc()
