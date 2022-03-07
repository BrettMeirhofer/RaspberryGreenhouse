import time
import GreenhouseFuncs as GHF
import sys
from bluetooth import Bulb
from bluetooth import get_rgb_hex


# Allows for manual deployment of relay commands without using the browser
if __name__ == '__main__':
    logger = GHF.create_logger("Control")
    command = sys.argv[1]

    if command == "relay":
        GHF.toggle_relay(sys.argv[2], int(sys.argv[3]))

    if command == "state":
        print(GHF.get_gpio_state(int(sys.argv[2])))

    if command == "light":
        command2 = sys.argv[2]
        bulb = Bulb("9C:04:A0:95:19:96")
        if command2 == "p":
            bulb.set_power(int(sys.argv[3]))

        if command2 == "f":
            bulb.flicker()

        if command2 == "c":
            command3 = sys.argv[3]
            if command3 == "r":
                bulb.write_data("33050dff000000000000000000000000000000c4")

            if command3 == "b":
                bulb.write_data("33050d0000ff00000000000000000000000000c4")

            if command3 == "g":
                bulb.write_data("33050d00ff0000000000000000000000000000c4")



