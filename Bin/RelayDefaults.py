from helper import GreenhouseFuncs as GHF
from helper import esp


# Uses the default states in config to update the relay states
def default_relays():
    logger = GHF.create_logger("Defaults")
    config_dict = GHF.open_config_dict("Config.json")
    for index, device_config in enumerate(config_dict["devices"].values()):
        if "default" in device_config:
            GHF.toggle_target_device(device_config, device_config["default"], config_dict, index)


if __name__ == '__main__':
    default_relays()
