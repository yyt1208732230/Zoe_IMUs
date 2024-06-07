import asyncio
import bleak
import device_model
import sys
import time

# Scanned devices
devices = []

def create_log_file():
    """Create a log file with a unique timestamp name."""
    timestamp = str(int(time.time()))
    filename = f'imuLog_{timestamp}.csv'
    f = open(filename, 'w')
    f.write("timestamp,AccX,AccY,AccZ,AsX,AsY,AsZ,AngleX,AngleY,AngleZ,HX,HY,HZ")
    return f

async def scan():
    """Scan for Bluetooth devices and filter by name containing 'HC'."""
    global devices
    find = []
    print("Searching for Bluetooth devices......")
    try:
        devices = await bleak.BleakScanner.discover()
        print("Search ended")
        for d in devices:
            if d.name and "HC" in d.name:
                find.append(d)
                print(d)
        if not find:
            print("No devices found in this search!")
    except Exception as ex:
        print("Bluetooth search failed to start")
        print(ex)

def dict_values_to_string(input_dict):
    """Convert dictionary values to a CSV string."""
    values_as_strings = map(str, input_dict.values())
    result_string = ','.join(values_as_strings)
    return result_string

def updateData(DeviceModel, f):
    """Handle updates to device data."""
    print(DeviceModel.deviceData)
    f.write('\n' + dict_values_to_string(DeviceModel.deviceData))

async def main():
    """Main function to handle device scanning and connection."""
    f = create_log_file()

    await scan()
    
    device_mac = None
    user_input = '00:0C:BF:08:26:66'
    for device in devices:
        if device.address == user_input:
            device_mac = device.address
            break
    
    if device_mac:
        device = device_model.DeviceModel("MyBle5.0", device_mac, lambda data: updateData(data, f))
        await device.openDevice()
    else:
        print("No Bluetooth device corresponding to Mac address found!!")
        f.close()

if __name__ == '__main__':
    asyncio.run(main())
