from TempRegulator import temp_errors
import GreenhouseFuncs as GHF


config_dict = GHF.open_config_dict("Config.json")
temp_errors(0, config_dict, None)
