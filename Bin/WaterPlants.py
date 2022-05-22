import time
from helper import GreenhouseFuncs as GHF


# Toggles a pump on a Tasmota Relay for a duration in order to water plants
def enable_pump():
    logger = GHF.create_logger("WaterPlants")
    config_dict = GHF.open_config_dict("Config.json")
    if config_dict["watering"]:
        pump_relay = config_dict["pump_relay"]
        GHF.toggle_device(pump_relay, True)
        time.sleep(config_dict["watering_duration"])
        GHF.toggle_device(pump_relay, False)
        logger.info("Successfully watered plants")


if __name__ == '__main__':
    enable_pump()


