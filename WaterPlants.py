import GreenhouseFuncs
import time


def enable_pump():
    watering_duration = 10
    GreenhouseFuncs.toggle_relay(2, 1)
    time.sleep(watering_duration)
    GreenhouseFuncs.toggle_relay(2, 0)


if __name__ == '__main__':
    enable_pump()
