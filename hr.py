import asyncio
import bitstruct
import struct
from bleak import BleakClient

HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"

async def run(address):

    async with BleakClient(address) as client:
        print("Connected: {0}".format(client.is_connected))

        def hr_val_handler(sender, data):
            """Simple notification handler for Heart Rate Measurement."""
            (unused, rr_int, nrg_expnd, snsr_cntct_spprtd, snsr_detect, hr_fmt) \
                = bitstruct.unpack("b3b1b1b1b1b1", data)
            if hr_fmt:
                hr_val, = struct.unpack_from("<H", data, 1)  # uint16
            else:
                hr_val, = struct.unpack_from("<B", data, 1)  # uint8
            print("HR: {0:3} bpm. Complete raw data: {1} ".format(hr_val, data.hex(sep=':')))

        await client.start_notify(HR_MEAS, hr_val_handler)

        while await client.is_connected:
            await asyncio.sleep(1)

#  E7:AC:D1:1B:B2:17 WHOOP 4A0393167 (dennis's)
if __name__ == "__main__":
    while True:
        address = ("E7:AC:D1:1B:B2:17")  # Change to address of device
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(address))
        print('reconnecting...')
