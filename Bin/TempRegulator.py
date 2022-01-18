import board
import adafruit_ahtx0
import adafruit_tca9548a
import datetime
import GreenhouseFuncs as GHF
from SendData import send_sensor_data


# Maintains greenhouse temperature by toggling a heater on a Tasmota relay based on temperature reported from sensors
# Sends heater status and sensor data to a remote web server for ingesting into a database
def handle_temp():
    config_dict = GHF.open_config_dict("Config.json")
    logger = GHF.create_logger()

    i2c = board.I2C()  # uses board.SCL and board.SDA
    tca = adafruit_tca9548a.TCA9548A(i2c)
    multi_ports = [0, 1, 2]
    port_names = ["Upper T/H", "Lower T/H", "System T/H"]

    temps = []
    web_json = {"date": datetime.datetime.now().strftime("%Y%m%d%H%M"), "readings": []}
    try:
        for index, port in enumerate(multi_ports):
            try:
                sensor = adafruit_ahtx0.AHTx0(tca[port])
                sensor_temp = round(sensor.temperature, 1)
                sensor_humd = round(sensor.relative_humidity, 1)
                web_json["readings"].extend([sensor_temp, sensor_humd])
                temps.append(sensor_temp)
            except ValueError:
                logger.error("Sensor {} is offline".format(port_names[index]))
    except OSError:
        logger.error("Multiplexer is offline")

    avg_temp = (temps[0] + temps[1]) / 2
    enable_heater = avg_temp < config_dict["heater_temp"]
    web_json["heater"] = int(enable_heater)
    GHF.toggle_relay(1, enable_heater)
    send_sensor_data(web_json, "/admin/Temp/")

    # Need a way to remember errors to prevent email spamming
    """
    if avg_temp > config_dict["too_hot"]:
        logger.error("Greenhouse Overheating")
        send_email("Greenhouse Overheating")

    if avg_temp < config_dict["too_cold"]:
        logger.error("Greenhouse Too Cold")
        send_email("Greenhouse Too Cold")
    """


if __name__ == '__main__':
    handle_temp()

# Add Hot/Cold Emails
# Add Data emails
