import flask
from flask import request
from flask import render_template
import Control
import GreenhouseFuncs as GHF

app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show errors in browser


# Provides a list of all animals when accessed with no args
# If an id is provided the details of a specific animal are retrieved
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/control', methods=['POST'])
def lights_on():
    logger = GHF.create_logger("ControlServer")
    device = request.args.get('device', type=str)
    power = request.args.get('power', default=1, type=int)
    logger.error(device)
    GHF.toggle_device(device, power)
    return '', 204


GHF.create_logger("ControlServer")
app.run(host="0.0.0.0")
