import RPi.GPIO as GPIO
from hcsr04sensor import sensor
import GreenhouseFuncs
import datetime


def record_water():
    trig = 4
    echo = 17

    data_file, writer = GreenhouseFuncs.get_data_file("Water")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    x = sensor.Measurement(trig, echo)
    distance_warm = x.raw_distance()
    distance_warm = round(distance_warm * 0.393701, 2)
    current_time = datetime.datetime.now().strftime("%H%M")
    writer.writerow([current_time, distance_warm])
    data_file.close()
    GPIO.cleanup((trig, echo))


if __name__ == '__main__':
    record_water()
