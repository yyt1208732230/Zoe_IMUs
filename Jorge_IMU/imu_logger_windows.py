#!/usr/bin/env python
"""
IMU Data logger for Windows
imu_logger_windows.py

Author: Nik Martelaro (original Linux version)
Modified for Windows compatibility

Purpose: Log data from an in-car IMU to a simple csv file. Timestamp every data
entry for data synchronization.
"""

import paho.mqtt.client as mqtt
import serial
import time
import sys, traceback
import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

def main():
    # The COM port will need to be adjusted to match the port your device is connected to.
    # You can find this in the Device Manager under "Ports (COM & LPT)".
    # Alternatively, you can write a function to list all available ports and select the correct one.
    imu_com_port = 'COM4'  # Example COM port, adjust as necessary

    part_path = '.'

    # Connect to the serial port
    ser = serial.Serial()
    ser.port = imu_com_port  # Use the COM port identified
    ser.baudrate = 9600
    ser.timeout = 1
    ser.open()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,'IMU')
    client.connect('localhost', 1883, 60)
    client.loop_start()

    # Setup the csv file to save the data
    f = open(part_path + '/' + 'imuLog_' +  str(int(time.time())) + '.csv', 'w')
    f.write("timestamp,X,Y,Z,SYS_calibration,GYRO_calibration,ACCEL_calibration,MAG_calibration")

    try:
        print('Now Logging IMU')
        while True:
            imuData = ser.readline()
            if len(imuData) > 0:
                # Log the system timestamp (unix) and then the data
                f.write(str(time.time()) + ',' + imuData.decode("utf-8"))
                datastream = str(imuData.decode("utf-8"))
                datastream = datastream.replace('\r\n', '')
                client.publish('key/IMU/all', datastream)

    except KeyboardInterrupt:
        print("\nShutdown requested...exiting IMU logger")
        # Close things cleanly
        client.loop_stop()
        f.close()
        ser.close()

    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

if __name__ == "__main__":
    main()
