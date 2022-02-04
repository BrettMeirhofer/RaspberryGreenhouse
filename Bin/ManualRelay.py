import time
import GreenhouseFuncs as GHF
import sys


# Allows for manual deployment of relay commands without using the browser
if __name__ == '__main__':
    logger = GHF.create_logger("ManualRelay")
    GHF.toggle_relay(sys.argv[1], int(sys.argv[2]))
