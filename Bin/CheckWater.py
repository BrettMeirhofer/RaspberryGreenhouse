import RPi.GPIO as GPIO
from hcsr04sensor import sensor
from helper.SendData import send_sensor_data
from helper import GreenhouseFuncs as GHF
from helper import esp


# Records water level and sends it to a remote web server
def record_water():
    logger = GHF.create_logger("CheckWater")
    config_dict = GHF.open_config_dict("Config.json")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    json_data = {"date": GHF.c_date(), "readings": []}
    for x in config_dict["level_sensors"]:
        if "ble_addr" in x:
            distance_warm = esp.get_sonar(x["ble_addr"])
        else:
            trig = x["trig"]
            echo = x["echo"]
            measure_object = sensor.Measurement(trig, echo)
            distance_warm = round(measure_object.raw_distance(), 4)
            GPIO.cleanup((trig, echo))

        json_data["readings"].append({"r": distance_warm, "s": x["id"]})

    print(json_data)
    send_sensor_data(json_data, "/admin/upload_readings/")


if __name__ == '__main__':
    record_water()

# Water level low email
