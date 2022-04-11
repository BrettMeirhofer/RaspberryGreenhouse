import flask
from flask import request, render_template
import json
from helper import GreenhouseFuncs as GHF
from helper.bluetooth import Bulb

app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = False  # allow to show errors in browser


# Provides a list of all animals when accessed with no args
# If an id is provided the details of a specific animal are retrieved
@app.route('/', methods=['GET'])
def home():
    resp = flask.Response(render_template("index.html"))
    resp.headers["Pragma-directive"] = "no-cache"
    resp.headers["Cache-directive"] = "no-cache"
    resp.headers["Cache-control"] = "no-cache, no-store"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = 0
    return resp


@app.route('/control', methods=['POST'])
def lights_on():
    logger = GHF.create_logger("ControlServer")
    device = request.args.get('device', type=str)
    power = request.args.get('power', default=1, type=int)
    color = request.args.get('color', default="", type=str)
    if color == "":
        GHF.toggle_device(device, power)
    else:
        bulb = Bulb("9C:04:A0:95:19:96")
        bulb.change_color_hex(color)

    return '', 204


@app.route('/toggles', methods=['GET'])
def get_toggles():
    config_dict = GHF.open_config_dict("Config.json")
    output_dict = {"devices": []}
    for device in config_dict["devices"]:
        state = GHF.get_device_state(device)
        output_dict["devices"].append({"name": device["name"], "type": device["type"], "state": state})
    return json.dumps(output_dict)


@app.route('/colors', methods=['GET'])
def get_colors():
    config_dict = GHF.open_config_dict("Config.json")
    return json.dumps({"colors": config_dict["colors"]})







GHF.create_logger("ControlServer")
app.run(host="0.0.0.0")
