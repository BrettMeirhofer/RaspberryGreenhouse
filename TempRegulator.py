import board
import adafruit_ahtx0
import adafruit_tca9548a
import datetime
import GreenhouseFuncs
import os
import json


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
    try:
        for index, port in enumerate(multi_ports):
            try:
                sensor = adafruit_ahtx0.AHTx0(tca[port])
                sensor_temp = round(sensor.temperature, 1)
                sensor_humd = round(sensor.relative_humidity, 1)
                temp_f = round((sensor_temp * (9/5)) + 32,2)
                writer.writerow([str(port), temp_f, sensor_humd,
                                 datetime.datetime.now().strftime("%H%M")])
                temps.append(sensor_temp)
            except ValueError:
                logger.error("Sensor {} is offline".format(port_names[index]))
    except OSError:
        logger.error("Multiplexer is offline")

    avg_temp = (temps[0] + temps[1]) / 2
    enable_heater = avg_temp < heater_temp
    GreenhouseFuncs.toggle_relay(1, enable_heater)
    if enable_heater:
        logger.info("Heater enabled")
    else:
        logger.info("Heater disabled")

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

# Handle Water Level on timer
# Check Moisture Level
# Check light level
# Send Emails upon Error
# If critical error write to a json file to shut subsystem down for later runs. Requires manual reset
# Manual reset of JSON file to re-enable subsystem
# Replacing writing to info log with POSTing to Django server
# Switch on a GPIO instead of
