#!/usr/bin/env python
"""
IMU Data logger
imu_logger.py

Author: Nik Martelaro
Last updated: 26 Jan 2017

Purpose: Log data from the in car IMU to a simple csv file. Timestamp every data
entry for data synchornization.
"""
import paho.mqtt.client as mqtt
import serial
import time
import sys, traceback
import pyudev
import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

def main():
	# connect to the correct arduino and get partcipant file path
	part_path = sys.argv[1]
	context= pyudev.Context()
	adafruit_metros= context.list_devices(subsystem='tty', ID_VENDOR='Silicon_Labs')
	imu=[d for d in adafruit_metros if d.properties['ID_SERIAL_SHORT']=='0182ED97'][0] #0182ED97 is the ID associated with the Metro Mini on the IMU board
	imu_path=imu.properties['DEVPATH'].split('tty/')[-1]

	#connect on serial
	ser = serial.Serial()
	ser.port = "/dev/"+imu_path
	ser.baudrate = 9600
	ser.timeout = 1
	ser.open()

	client = mqtt.Client('IMU')
	client.connect('localhost', 1883, 60)
	client.loop_start()

	# client.publish('key/IMU/all',
	# 			   "timestamp,X,Y,Z,SYS_calibration,GYRO_calibration,ACCEL_calibration,MAG_calibration\r\n")

	# setup the csv file to save the data
	f = open(part_path + '/' + 'imuLog_' +  str(int(time.time())) + '.csv', 'w')
	f.write("timestamp,X,Y,Z,SYS_calibration,GYRO_calibration,ACCEL_calibration,MAG_calibration");


	try:
		print('Now Logging IMU')
		while True:
			imuData = ser.readline()
			if len(imuData)>0:
				# log the system timestamp (unix) an then the data
				f.write(str(time.time()) + ',' + imuData.decode("utf-8"))
				datastream = str(imuData.decode("utf-8"))
				datastream = datastream.replace('\r\n', '')
				client.publish('key/IMU/all', datastream)
				# dataStream = imuData.decode("utf-8").split(",")
				# client.publish('key/IMU/X', dataStream[0])
				# client.publish('key/IMU/Y', dataStream[1])
				# client.publish('key/IMU/Z', dataStream[2])
				# client.publish('key/IMU/SYS_cal', dataStream[3])
				# client.publish('key/IMU/GYRO_cal', dataStream[4])
				# client.publish('key/IMU/ACCEL_cal', dataStream[5])
				# client.publish('key/IMU/MAG_cal', dataStream[6])

	except KeyboardInterrupt:
		print("\nShutdown requested...exiting IMU logger")
		# close things cleanly
		client.loop_stop()
		f.close()
		ser.close()
		# quit_gracefully(f,ser)

	except Exception:
		traceback.print_exc(file=sys.stdout)
		sys.exit(0)

if __name__ == "__main__":
    main()
