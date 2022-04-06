import RPi.GPIO as GPIO
from hcsr04sensor import sensor
from Bin.helper.SendData import send_sensor_data
from Bin.helper import GreenhouseFuncs as GHF


# Records water level and sends it to a remote web server
def record_water():
    logger = GHF.create_logger("CheckWater")
    config_dict = GHF.open_config_dict("Config.json")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    json_data = {"date": GHF.c_date(), "readings": []}
    for x in config_dict["level_sensors"]:
        trig = x["trig"]
        echo = x["echo"]
        measure_object = sensor.Measurement(trig, echo)
        distance_warm = measure_object.raw_distance()
        json_data["readings"].append({"r": round(distance_warm, 4), "s": x["id"]})
        send_sensor_data(json_data, "/admin/Water/")
        GPIO.cleanup((trig, echo))

    send_sensor_data(json_data, "/admin/upload_readings/")


if __name__ == '__main__':
    record_water()

# Water level low email
