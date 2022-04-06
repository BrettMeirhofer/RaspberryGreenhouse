from Bin.helper import GreenhouseFuncs as GHF


# Uses the default states in config to update the relay states
def default_relays():
    config_dict = GHF.open_config_dict("Config.json")
    for device_config in config_dict["devices"]:
        if "default" in device_config:
            GHF.toggle_gpio(device_config["gpio"], device_config["default"])


if __name__ == '__main__':
    default_relays()
