# IMU Data Collection Manual

![IMU Visulization Demo](https://github.com/yyt1208732230/Zoe_IMUs/blob/main/20240610084013_IMU_headmovement.png "IMU Demo")

# WIT IMU Recording Processing with RTMaps (MQTT Protocol)

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
   - (optional) if is new set-up in the server computer, set user name&password first with `mosquitto_passwd -c  pwfile.example admin`, and pwd with `admin`.
   - `mosquitto.exe -c mosquitto.conf`
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

---

# WIT IMU Recording Processing with RTMaps (UDP Protocol)

...

![BT Adapter](https://github.com/yyt1208732230/Zoe_IMUs/blob/main/WIT_BWT901CL/images/UGREEN%20Bluetooth%205.4%20Adapter.png "UGREEN BT Adapter")

![IMU](https://github.com/yyt1208732230/Zoe_IMUs/blob/main/WIT_BWT901CL/images/WIT-BTIMU.png "WIT_BWT901CL")

---

# Test Cases (WIT901CL)

| Test ID | Test Category                  | Test Description                                                                                     | Test Result (√ Passed or x Failed) | Protocol | Return Rate | Bandwith | Compilation language | Distance | Adapter |
| ------- | ------------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------- | -------- | ----------- | -------- | -------------------- | -------- | ------- |
| A1      | Sampling Rate Stability        | Test 10Hz in Python MQTT                                                                             | √                                  | MQTT     | 200Hz       | 256Hz    | Python               | ±3m     | UGREEN  |
| A2      | Sampling Rate Stability        | Test 40Hz in Python MQTT                                                                             | √                                  | MQTT     | 200Hz       | 256Hz    | Python               | ±3m     | UGREEN  |
| A3      | Sampling Rate Stability        | Test 10Hz in Python UDP                                                                              | √ (not stable)                     | UDP      | 10Hz        | 256Hz    | Python               | ±3m     | UGREEN  |
| A4      | Sampling Rate Stability        | Test 40Hz in Python UDP                                                                              | √ (not stable)                     | UDP      | 200Hz       | 256Hz    | Python               | ±3m     | UGREEN  |
| A5      | Sampling Rate Stability        | Test 100Hz in C++ MQTT                                                                               |                                     | MQTT     | 200Hz       | 20Hz     | C++                  | ±3m     | UGREEN  |
| B1      | Bluetooth Connection Stability | Test with cheap Bluetooth receiver (toocki) for 2+ hours & movement within 2m                        | X                                   | MQTT     | 200Hz       | 256Hz    | Python               | ±1m     | toocki  |
| B2      | Bluetooth Connection Stability | Test with high-end Bluetooth receiver (UGreen) for 2+ hours & movement within 2m                    | -                                   |          |             |          |                      |          |         |
| B3      | Bluetooth Connection Stability | Test with WIT HID (manufacturer-specified model) Bluetooth dongle for 2+ hours & movement within 2m |                                     |          |             |          |                      |          |         |
| C1      | Robustness                     | [Better to have] Reconnect after IMU actively disconnects                                            | X                                   | MQTT     | 10Hz        | 20Hz     | Python               | ±1m     | toocki  |
| C2      | Robustness                     | [Better to have] Reconnect after IMU passively disconnects (IMU turn-off)                            | X                                   | MQTT     | 10Hz        | 20Hz     | Python               | ±1m     | toocki  |
| C3      | Robustness                     | Reconnect after disconnection due to long distance (3m+)                                             | √                                  | MQTT     | 200Hz       | 256Hz    | Python               | ±4m     | UGREEN  |
| C4      | Robustness                     | Long-term connection test (2 hours)                                                                  | √                                  | UDP      | 100Hz       | 20Hz     | Python               | <20cm    | toocki  |
| C5      | Robustness                     | Reconnect after broker server is shut down and restarted                                             | -                                   |          |             |          |                      |          |         |

# Issue Logs & Solution

## A. Bleak Device Not Found Error :

- Source: Python Publisher Script `bt2mqtt_publisher_imu_WITt901cl`.
- Details:

```Found
Initialize device model
Opening device......
...
 File "C:\ProgramData\anaconda3\Lib\site-packages\bleak\backends\winrt\client.py", line 293, in connect
    raise BleakDeviceNotFoundError(
bleak.exc.BleakDeviceNotFoundError: Device with address 00:0C:BF:08:26:66 was not found.
```

- Solution:

```
1. Terminate Script `bt2mqtt_publisher_imu_WITt901cl` & 
2. turn off IMU & 
3. wait for 15 seconds & 
4. retry *STEP 4*.
```
