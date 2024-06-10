import asyncio
import bleak
import device_model
import sys
import time
import socket

# Scanned devices
devices = []

def create_log_file():
    """Create a log file with a unique timestamp name.
    创建带有唯一时间戳名称的日志文件。
    """
    timestamp = str(int(time.time()))
    filename = f'imuLog_{timestamp}.csv'
    f = open(filename, 'w')
    f.write("timestamp,AccX,AccY,AccZ,AsX,AsY,AsZ,AngleX,AngleY,AngleZ,HX,HY,HZ")
    return f

async def scan():
    """Scan for Bluetooth devices and filter by name containing 'HC'.
    扫描蓝牙设备，并根据名称过滤包含'HC'的设备。
    """
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
    """Convert dictionary values to a CSV string.
    将字典值转换为CSV字符串。
    """
    values_as_strings = map(str, input_dict.values())
    result_string = ','.join(values_as_strings)
    return result_string

def updateData(DeviceModel, sock, addr, f=None):
    """Handle updates to device data and send it to the specified port.
    处理设备数据更新并将其发送到指定端口。
    """
    data_str = dict_values_to_string(DeviceModel.deviceData)
    # print(DeviceModel.deviceData)
    # f.write('\n' + data_str)
    sock.sendto(data_str.encode(), addr)


async def main():
    """Main function to handle device scanning and connection.
    主函数，处理设备扫描和连接。
    """
    # Replace with your target IP and port
    target_ip = "127.0.0.1"
    target_port = 7777
    addr = (target_ip, target_port)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"UDP config target IP: {target_ip}, target port: {target_port}")
    await scan()
    
    device_mac = None
    user_input = '00:0C:BF:08:26:66'
    for device in devices:
        if device.address == user_input:
            device_mac = device.address
            break
    
    if device_mac:
        # f = create_log_file()
        # device = device_model.DeviceModel("MyBle5.0", device_mac, lambda data: updateData(data, sock, addr, f))
        device = device_model.DeviceModel("MyBle5.0", device_mac, lambda data: updateData(data, sock, addr))
        await device.openDevice()
        # f.close()
    else:
        print("No Bluetooth device corresponding to Mac address found!!")

if __name__ == '__main__':
    asyncio.run(main())
