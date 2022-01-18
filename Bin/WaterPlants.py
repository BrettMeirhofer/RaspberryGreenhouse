import time
import GreenhouseFuncs as GHF


# Toggles a pump on a Tasmota Relay for a duration in order to water plants
def enable_pump():
    config_dict = GHF.open_config_dict("Config.json")
    GHF.toggle_relay(2, 1)
    time.sleep(config_dict["watering_duration"])
    GHF.toggle_relay(2, 0)


if __name__ == '__main__':
    enable_pump()
