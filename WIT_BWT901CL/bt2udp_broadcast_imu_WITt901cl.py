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

async def scan(user_input):
    """Continuously scan for the specified Bluetooth device until found.
    持续扫描指定的蓝牙设备直到找到。
    """
    device_mac = None
    while not device_mac:
        print("Searching for Bluetooth device with address:", user_input)
        try:
            await asyncio.sleep(10)  # Wait for 10 seconds before trying
            devices = await bleak.BleakScanner.discover()
            for d in devices:
                if d.address == user_input:
                    device_mac = d.address
                    print(f"Found device: {d}")
                    break
            if not device_mac:
                print("Device not found, retrying...")
        except Exception as ex:
            print("Bluetooth search failed to start")
            print(ex)
            await asyncio.sleep(10)  # Wait for 10 seconds before retrying
    return device_mac

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
    # Data log configuration
    is_csv = False

    # Replace with your target IP and port
    target_ip = "127.0.0.1"
    target_port = 7777
    addr = (target_ip, target_port)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"UDP config target IP: {target_ip}, target port: {target_port}")

    device_mac = None
    user_input = '00:0C:BF:08:26:66'
    device_mac = await scan(user_input)
    
    device = None
    try:
        if device_mac:
            # start csv log
            if is_csv:
                f = create_log_file()
            else: 
                f= None
            # start reading imu data
            device = device_model.DeviceModel("MyBle5.0", device_mac, lambda data: updateData(data, sock, addr))
            await device.openDevice()
            # close csv log
            if is_csv:
                f.close()
        else:
            print("No Bluetooth device corresponding to Mac address found!!")
    except Exception as ex:
            print(ex)

if __name__ == '__main__':
    asyncio.run(main())
