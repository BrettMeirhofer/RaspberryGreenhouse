import requests
import json
import GreenhouseFuncs as GHF


def send_sensor_data(json_data, endpoint):
    config_dict = GHF.open_config_dict("WebConfig.json")
    target_url = config_dict["website_url"] + endpoint
    headers = {"Authorization": config_dict["website_token"]}
    r = requests.post(target_url, data=json.dumps(json_data), headers=headers, allow_redirects=False)

