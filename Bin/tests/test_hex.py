import Bin.bluetooth

print(Bin.bluetooth.get_rgb_hex(255, 0, 0))
print(Bin.bluetooth.get_rgb_hex(255, 0, 0))
rgb = tuple(int("ff0000"[i:i + 2], 16) for i in (0, 2, 4))
print(rgb)
print(hex(rgb[0]).replace("0x", ""))
print(Bin.bluetooth.get_rgb_hex(*rgb))