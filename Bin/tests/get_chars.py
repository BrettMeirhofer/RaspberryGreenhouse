import asyncio
from bleak import BleakClient
import sys

address = "34:94:54:25:E3:12"


async def main(address: str):
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)
            for x in service.characteristics:
                print(x)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else address))
