import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import serial
import time
import sys
import traceback
import signal
import paho.mqtt.client as mqtt

signal.signal(signal.SIGINT, signal.default_int_handler)

def main():
    imu_com_port = 'COM6'  # Example COM port, adjust as necessary

    ser = serial.Serial()
    ser.port = imu_com_port
    ser.baudrate = 9600
    ser.timeout = 1
    ser.open()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,'IMU')
    client.connect('localhost', 1883, 60)
    client.loop_start()

    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-100, 100])
    ax.set_ylim([-100, 100])
    ax.set_zlim([-100, 100])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('IMU Real-time Visualization')

    data = np.zeros((3, 1))
    line, = ax.plot(data[0, :], data[1, :], data[2, :], marker='o', linestyle='-')
    trajectory = []

    try:
        print('Now Visualizing IMU')
        while True:
            imuData = ser.readline()
            if len(imuData) > 0:
                decoded_data = imuData.decode("utf-8").rstrip('\r\n')
                datastream = decoded_data.split(',')
                if len(datastream) == 22:  # Ensure complete data is received
                    acceleration = [float(datastream[13]), float(datastream[14]), float(datastream[15])]
                    # Update data
                    data[0] += acceleration[0] * 0.1  # Assuming 0.1 second sampling time
                    data[1] += acceleration[1] * 0.1
                    data[2] += acceleration[2] * 0.1
                    # Store data for trajectory
                    trajectory.append((data[0, 0], data[1, 0], data[2, 0]))
                    # Update visualization
                    line.set_xdata(data[0, :])
                    line.set_ydata(data[1, :])
                    line.set_3d_properties(data[2, :])
                    line.set_marker('o')  # Set marker for the current position
                    line.set_linestyle('-')  # Set linestyle for the trajectory
                    line.set_markevery(-1)  # Only show marker at the current position
                    ax.plot([x[0] for x in trajectory], [y[1] for y in trajectory], [z[2] for z in trajectory],
                            color='gray', alpha=0.5)  # Plot trajectory
                    plt.pause(0.1)  # Pause for a short time to update the plot

    except KeyboardInterrupt:
        print("\nShutdown requested...exiting IMU visualization")
        client.loop_stop()
        ser.close()

    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

if __name__ == "__main__":
    main()
