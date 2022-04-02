import time


try:
    import pexpect
except ImportError:
    pass


class Esp:
    mac = ""

    gatt = None

    def __init__(self, mac):
        self.gatt = pexpect.spawn('gatttool -I')
        self.mac = mac

    def read_data(self, handle):
        self.gatt.sendline(f"connect {self.mac}")
        try:
            self.gatt.expect("Connection successful", timeout=5)
        except pexpect.exceptions.TIMEOUT:
            print(f"Failed to connect")
            return

        print("Connection success")
        line = f"char-read-cmd {handle}"
        self.gatt.sendline(line)
        self.gatt.expect(".*")
        self.gatt.sendline("disconnect")
        self.gatt.expect(".*")
        print(self.gatt.read())


my_esp = Esp("34:94:54:25:E3:12")
my_esp.read_data("0x0015")

#gatttool -b 34:94:54:25:E3:12 -I
#gatttool -t random -b 30:C6:F7:0B:4E:D6 -I
#connect 30:C6:F7:0B:4E:D6
#9C:04:A0:95:19:96
#bluetoothctl pair 30:C6:F7:0B:4E:D6
#gatttool -b 9C:04:A0:95:19:96 -I
#char-read-hnd 0x0016