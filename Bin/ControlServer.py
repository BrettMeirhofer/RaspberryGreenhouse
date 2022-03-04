import flask
from flask import request
from flask import render_template

app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show errors in browser


# Provides a list of all animals when accessed with no args
# If an id is provided the details of a specific animal are retrieved
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

app.run(host="0.0.0.0")
