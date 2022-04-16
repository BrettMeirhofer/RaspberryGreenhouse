import requests
from helper import esp
from helper.bluetooth import Bulb
import json


try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


# Generic device that can be toggled
class Device:
    name = "Generic"
    allow_read = True
    state = 0

    def read_state(self):
        return self.state

    def set_state(self, state):
        return 0

    pass


# Device that can be controlled via web requests to Tasmota software
class TasmotaDevice(Device):
    relay_id = 0
    allow_read = False
    ip_address = ""

    def set_state(self, state):
        target_url = "http://{}/cm?cmnd=Power{}%20{}".format(self.ip_address, self.relay_id, state)
        requests.get(url=target_url)

    def read_state(self):
        toggle_map = {"ON": 1, "OFF": 0}
        relay = "POWER" + str(self.relay_id)
        target_url = "http://{}/cm?cmnd=".format(self.ip_address) + relay
        key = json.loads(requests.get(url=target_url).json())[relay]
        return toggle_map[key]
        

# Device that can be controlled via GPIO pins
class GPIODevice(Device):
    pin = ""
    default = None

    def set_state(self, state):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if state:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)

    def read_state(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            return not GPIO.input(self.pin)
        except NameError:
            return 0

    def apply_default(self):
        if self.default is not None:
            self.set_state(self.default)


# Device that can be controlled via Bluetooth LE
class BTDevice(Device):
    mac = ""
    attribute = ""

    def set_state(self, state):
        esp.update_relay(self.mac, self.attribute, state)


class H6008(BTDevice):
    mac = ""
    attribute = ""
    allow_read = False

    def set_state(self, state):
        bulb = Bulb(self.mac)
        bulb.set_power(state)



