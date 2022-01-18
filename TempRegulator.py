import board
import adafruit_ahtx0
import adafruit_tca9548a
import datetime
import GreenhouseFuncs
import os
import json
from SendData import send_sensor_data


def handle_temp():
    config_file = open(os.path.join(os.path.dirname(__file__), "Config.json"))
    config_dict = json.loads(config_file.read())
    data_file, writer = GreenhouseFuncs.get_data_file("Temp")
    logger = GreenhouseFuncs.create_logger()
    heater_temp = 24
    max_temp = 38
    min_temp = 4.5

    i2c = board.I2C()  # uses board.SCL and board.SDA

    tca = adafruit_tca9548a.TCA9548A(i2c)

    multi_ports = [0, 1, 2]
    port_names = ["Upper T/H", "Lower T/H", "System T/H"]

    temps = []
    web_json = {"date": datetime.datetime.now().strftime("%Y%m%d%H%M")}
    data_row = [datetime.datetime.now().strftime("%H%M")]
    sensor_data = []
    try:
        for index, port in enumerate(multi_ports):
            try:
                sensor = adafruit_ahtx0.AHTx0(tca[port])
                sensor_temp = round(sensor.temperature, 1)
                sensor_humd = round(sensor.relative_humidity, 1)
                sensor_data.extend([sensor_temp, sensor_humd])
                temps.append(sensor_temp)
            except ValueError:
                logger.error("Sensor {} is offline".format(port_names[index]))
    except OSError:
        logger.error("Multiplexer is offline")

    web_json["readings"] = sensor_data
    avg_temp = (temps[0] + temps[1]) / 2
    enable_heater = avg_temp < heater_temp
    web_json["heater"] = int(enable_heater)
    GreenhouseFuncs.toggle_relay(1, enable_heater)
    data_row.append(sensor_data)
    data_row.insert(1, int(enable_heater))
    writer.writerow(data_row)

    send_sensor_data(web_json, "/admin/Temp/")


    # Need a way to remember errors to prevent email spamming
    """
    if avg_temp > max_temp:
        logger.error("Greenhouse Overheating")
        send_email("Greenhouse Overheating")

    if avg_temp < max_temp:
        logger.error("Greenhouse Too Cold")
        send_email("Greenhouse Too Cold")
    """

    data_file.close()


if __name__ == '__main__':
    handle_temp()

# Add Hot/Cold Emails
# Add Data emails
