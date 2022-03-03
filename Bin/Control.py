import time
import GreenhouseFuncs as GHF
import sys
import pexpect


class BlueBulb:
    mac = "9C:04:A0:95:19:96"
    handle = 21
    handle_hex = "0x0011"
    off = "3301000000000000000000000000000000000032"
    on = "3301010000000000000000000000000000000033"
    gatt = None

    def __init__(self):
        self.gatt = pexpect.spawn('gatttool -I')

    def write_data(self, data):
        self.gatt.sendline(f"connect {self.mac}")
        try:
            self.gatt.expect("Connection successful", timeout=5)
        except pexpect.exceptions.TIMEOUT:
            print(f"Failed to connect")
            return

        print("Connection success")
        line = f"char-write-cmd {self.handle_hex} {data}"
        print(line)
        self.gatt.sendline(line)
        self.gatt.expect(".*")
        self.gatt.sendline("disconnect")
        self.gatt.expect(".*")

    def flicker(self):
        for x in range(5):
            self.write_data(self.on)
            time.sleep(3)
            self.write_data(self.off)
            time.sleep(3)

    def set_power(self, power):
        if power:
            self.write_data(self.on)
        else:
            self.write_data(self.off)


# Allows for manual deployment of relay commands without using the browser
if __name__ == '__main__':
    logger = GHF.create_logger("Control")
    command = sys.argv[1]
    if command == "relay":
        GHF.toggle_relay(sys.argv[2], int(sys.argv[3]))

    if command == "light":
        command2 = sys.argv[2]
        bulb = BlueBulb()
        if command2 == "p":
            bulb.set_power(int(sys.argv[3]))

        if command2 == "f":
            bulb.flicker()


