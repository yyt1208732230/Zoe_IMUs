from pynput import keyboard
import paho.mqtt.client as mqtt
import ssl
import time
import sys, traceback
import signal

signal.signal(signal.SIGINT, signal.default_int_handler)


def main():
    try:
        

        broker = "localhost"
        port = 1883
        topic = "clicker/all"

        # Create MQTT client
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,'IMU')
        client.connect(broker, port, 60)
        client.loop_start()

        # AWS client service
        # participant_path = sys.argv[1]
        # client = mqtt.Client('marker_aws')
        # client.connect('abcdefghifk-ats.iot.ap-southeast-2.amazonaws.com', 8883, 60)
        # client.tls_set(ca_certs='/home/carrsq/PycharmProjects/_XXX/Remote_communication/AmazonRootCA1.pem',
        #                certfile='/home/carrsq/PycharmProjects/_XXX/Remote_communication/_XXX_marker_abcdeec6cf-certificate.pem.crt',
        #                keyfile='/home/carrsq/PycharmProjects/_XXX/Remote_communication/_XXX_marker_abcdeec6cf-private.pem.key',
        #                cert_reqs=ssl.CERT_REQUIRED,
        #                tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        client.loop_start()

        # setup the txt file to save the data
        # f = open(participant_path + '/' + 'participant_keypoints_' + str(int(time.time())) + '.txt', 'w')
        # f.write("local|controler|message\n")
        print('Now logging participant keypoints')
        marks = 0

        # f= open(participant+"keypoints.txt", "w")
        def on_press(key):
            try:
                nonlocal marks
                if key == keyboard.Key.page_up:
                    # f.write(str(time.time()) + '|' + str(time.time()) + '|.' + '\n')
                    marks += 1
                    print("marked: " + str(marks))
                    client.publish(topic, str(marks))
                    print("Page Up key pressed")
                elif key == keyboard.Key.page_down:
                    marks += 1
                    print("marked: " + str(marks))
                    client.publish(topic, str(marks))
                    print("Page Down key pressed")
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        listener.start()

    except KeyboardInterrupt:
        print("\nShutdown requested...exiting mark logger")
        client.loop_stop()
        # close things cleanly
        # f.close()

    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
