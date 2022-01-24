import RPi.GPIO as GPIO
from hcsr04sensor import sensor
import datetime
from SendData import send_sensor_data
import GreenhouseFuncs as GHF


# Records water level and sends it to a remote web server
def record_water():
    logger = GHF.create_logger("CheckWater")
    config_dict = GHF.open_config_dict("Config.json")
    trig = 4
    echo = 17
    reservoir_height = config_dict["reservoir_height"]
    sensor_height = config_dict["water_sensor_dist"]
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    measure_object = sensor.Measurement(trig, echo)
    distance_warm = measure_object.raw_distance()
    water_percent = round(1 - ((distance_warm - sensor_height) / reservoir_height), 4)
    GPIO.cleanup((trig, echo))
    json_data = {"date": datetime.datetime.now().strftime("%Y%m%d%H%M"), "water_level": water_percent}
    send_sensor_data(json_data, "/admin/Water/")


if __name__ == '__main__':
    record_water()

# Water level low email
