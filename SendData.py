import requests
import json
import datetime
import os


def send_sensor_data(json_data, endpoint):
    config_file = open(os.path.join(os.path.dirname(__file__), "Config.json"))
    config_dict = json.loads(config_file.read())
    target_url = config_dict["website_url"] + endpoint
    headers = {"Authorization": config_dict["website_token"]}
    r = requests.post(target_url, data=json.dumps(json_data), headers=headers, allow_redirects=False)


def send_dummy_sensor_data():
    current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    data = {"date": current_date_time, "heater": 1, "readings": [25, 50, 24, 45, 24.5, 47]}
    send_sensor_data(data)
