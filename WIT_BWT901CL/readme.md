# WIT IMU Recording Processing with RTMaps
Please ensure the environment is fully set up before starting to publish data from the IMU sensor.

![Data transmission topology diagram](https://github.com/yyt1208732230/Zoe_IMUs/blob/main/WIT_BWT901CL/mqtt_server_mosquitto/MQTT.png "MQTT Topology")

## Step 1: Software Checklist (Installation)
1. **Install MQTT Broker (Server)**
   - Install Mosquitto:
     - [mosquitto-2.0.18a-install-windows-x86](https://mosquitto.org/files/binary/win64/mosquitto-2.0.18-install-windows-x64.exe)
     - [mosquitto-2.0.18a-install-windows-x64](https://mosquitto.org/files/binary/win32/mosquitto-2.0.18-install-windows-x86.exe)
   - Configuration:
     - Update `mosquitto.conf`:
       - Replace `mosquitto.conf` with the file in the repo folder (`mqtt_server_mosquitto/mosquitto.conf`)
       - OR update `listener 1883` and `allow_anonymous true`
     - Set default user:
       - Example: `mosquitto_passwd -c pwfile.example admin`
2. **Install MQTT Service Test Tool (Optional)**
   - Install MQTTBox
3. **Install Python**
   - Packages: `pip install bleak paho-mqtt`
4. **Install RTMaps (Subscriber)**

## Step 2: Hardware Checklist
1. IMU (WIT-T901CL)

## Step 3: Turn on the MQTT Server
1. Open CMD and navigate to the Mosquitto folder (the server).
  `cd mosquitto`
2. In the root folder of Mosquitto, execute: 
  `mosquitto.exe -c mosquitto.conf`
3. (Optional) Create a client and subscriber on MQTTBox. You will see the data stream under the topic.

## Step 4: Start Publishing Data from the Bluetooth IMU
1. Turn on the WIT IMU.
2. Wait for 10 seconds (initialization of the Bluetooth sensor).
3. In the IMU Python folder, execute: 
  `python bt2mqtt_publisher_imu_WITt901cl.py`
4. You will see the data log on the console.

## Step 5: Collect IMU Sensor Data
1. (Optional) Create a subscriber on MQTTBox. You will see the data stream under the topic.
2. Open the pre-set RTMaps and start recording data on the MQTT component.

# IMU Testing Checklist

| Test ID | Test Category                  | Test Description                                                                            | Test Result (√ or x) |
|---------|--------------------------------|---------------------------------------------------------------------------------------------|----------------------|
| A1      | Sampling Rate Stability Test   | Test 100Hz Python MQTT                                                                             |                      |
| A2      | Sampling Rate Stability Test   | Test 200Hz Python UDP                                                                              |                      |
| A3      | Sampling Rate Stability Test   | Test 200Hz C++ MQTT                                                                         |                      |
| B1      | Bluetooth Connection Stability | Test with cheap Bluetooth receiver (toocki) for 30 mins at 80% battery level                |                      |
| B2      | Bluetooth Connection Stability | Test with high-end Bluetooth receiver (UGreen) for 30 mins                                  |                      |
| B3      | Bluetooth Connection Stability | Test with WIT HID (manufacturer-specified model) Bluetooth receiver                         |                      |
| C1      | Robustness Test                | Reconnect after IMU actively disconnects                                                    |                      |
| C2      | Robustness Test                | Reconnect after IMU passively disconnects (shutdown)                                        |                      |
| C3      | Robustness Test                | Reconnect after disconnection due to long distance (3M)                                     |                      |
| C4      | Robustness Test                | Long-term connection test (2 hours)                                                         |                      |
| C5      | Robustness Test                | Reconnect after broker server is shut down and restarted                              |                      |
