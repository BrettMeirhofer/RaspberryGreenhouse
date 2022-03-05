import time

try:
    import pexpect
except ImportError:
    pass


def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h


def get_rgb_hex(r, g, b):
    bins = [51, 5, 13, r, g, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sig = 0
    for item in bins:
        sig = sig ^ item
    bins.append(sig)
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)


class Bulb:
    mac = "9C:04:A0:95:19:96"
    handle = 21
    handle_hex = "0x0011"
    off = "3301000000000000000000000000000000000032"
    on = "3301010000000000000000000000000000000033"

    gatt = None

    def __init__(self, mac):
        self.gatt = pexpect.spawn('gatttool -I')
        self.mac = mac

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

    def change_color(self, rgbt):
        r, g, b = rgbt
        hex_str = get_rgb_hex(r, g, b)
        self.write_data(hex_str)
        print(f"Changed {self.mac} color to {rgbt}")

    def change_color_hex(self, hex_color):
        self.change_color(tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)))


