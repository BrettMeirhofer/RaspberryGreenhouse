import time
import GreenhouseFuncs as GHF


# Toggles a pump on a Tasmota Relay for a duration in order to water plants
def enable_pump():
    logger = GHF.create_logger("WaterPlants")
    config_dict = GHF.open_config_dict("Config.json")
    GHF.toggle_relay(2, True)
    time.sleep(config_dict["watering_duration"])
    GHF.toggle_relay(2, False)
    logger.info("Successfully watered plants")


if __name__ == '__main__':
    enable_pump()
