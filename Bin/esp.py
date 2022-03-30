import time

"""
try:
    import pexpect
except ImportError:
    pass


class Esp:
    mac = "9C:04:A0:95:19:96"

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
        line = f"char-write-cmd {data}"
        print(line)
        self.gatt.sendline(line)
        self.gatt.expect(".*")
        self.gatt.sendline("disconnect")
        self.gatt.expect(".*")


my_esp = Esp("30:C6:F7:0B:4E:D6")
my_esp.write_data("31")
#gatttool -b 30:C6:F7:0B:4E:D6 -I
gatttool -t random -b 30:C6:F7:0B:4E:D6 -I
connect 30:C6:F7:0B:4E:D6
"""



import socket

serverMACAddress = '30:C6:F7:0B:4E:D6'
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()