"""
Scan/Discovery Async Iterator
--------------

Example showing how to scan for BLE devices using async iterator instead of callback function

Created on 2023-07-07 by bojanpotocnik <info@bojanpotocnik.com>

"""
import asyncio

from bleak import BleakScanner
from bleak.uuids import normalize_uuid_16


async def main():
    hr_svc = normalize_uuid_16(0x180D)
    async with BleakScanner() as scanner:
        print("Scanning...")

        print(f"\n    advertisement packets:")
        try:
            async for bd, ad in scanner.advertisement_data():
                #if bd.address != 'E7:AC:D1:1B:B2:17':
                #if not (ad.local_name or 'None').startswith('WHOOP'):
                    #continue
                if hr_svc not in ad.service_uuids:
                    continue
                print(f"         {bd.address} {ad.local_name}")
                #print(f"         service_uuids {ad.service_uuids}")
                #print(dir(ad))
                #print('bd', bd)
                #print('ad', ad)
                #print('ad.manufacturer_data', ad.manufacturer_data)
                #print('ad.platform_data', ad.platform_data)
                #print('ad.service_data', ad.service_data)
                #print(f"         {bd!r} with {ad!r}")
        except asyncio.exceptions.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
