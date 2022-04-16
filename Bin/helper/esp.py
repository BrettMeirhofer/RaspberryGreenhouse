import asyncio
from bleak import BleakClient
import time


# Sends a write request to a remote ble device which updates the server sonar value
# Then does a read request to get the resulting value
async def sonar(address: str):
    async with BleakClient(address) as client:
        await client.write_gatt_char(char_specifier="00002a6e-0000-1000-8000-00805f9b34fb", data=b"")
        time.sleep(1)
        value = await client.read_gatt_char(char_specifier="00002a6e-0000-1000-8000-00805f9b34fb")
        return int(value)


def get_sonar(address):
    return asyncio.run(sonar(address))


async def async_update_relay(address, char, state):
    async with BleakClient(address) as client:
        payload = str(1 - state).encode("UTF-8")
        await client.write_gatt_char(char_specifier=char, data=payload)


def update_relay(address, char, state):
    asyncio.run(async_update_relay(address, char, state))


# Reads a relay status on a bt device
# Inverts the output since gpio high turns off the relay
async def async_read_relay(address, char):
    async with BleakClient(address) as client:
        value = await client.read_gatt_char(char_specifier=char)
        return 1 - int(value)


def read_relay(address, char):
    return asyncio.run(async_read_relay(address, char))



