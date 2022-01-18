import RPi.GPIO as GPIO
from hcsr04sensor import sensor
import GreenhouseFuncs
import datetime
from SendData import send_sensor_data


def record_water():
    trig = 4
    echo = 17
    reservoir_height = 30.48
    sensor_height = 17.78
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    measure_object = sensor.Measurement(trig, echo)
    distance_warm = measure_object.raw_distance()
    water_percent = round((distance_warm - sensor_height) / reservoir_height, 4)
    GPIO.cleanup((trig, echo))
    json_data = {"date": datetime.datetime.now().strftime("%Y%m%d%H%M"), "water_level": water_percent}
    send_sensor_data(json_data, "/admin/Water/")


if __name__ == '__main__':
    record_water()
