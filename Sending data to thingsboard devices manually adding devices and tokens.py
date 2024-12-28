import paho.mqtt.client as mqtt
import json
import random
import time
import warnings

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

THINGSBOARD_HOST = '13.234.60.181'

# Replace these with the access tokens for your 10 devices
DEVICE_TOKENS = {
    # 'PRE 1167': 'pre1167'
    'PRE 1169': 'pre1169'
    # 'Device 1': 'Device_1',
    # 'Device 2': 'Device_2',
    # 'Device 3': 'Device_3',
    # 'Device 4': 'Device_4',
    # 'Device 5': 'Device_5',
    # 'Device 6': 'Device_6',
    # 'Device 7': 'Device_7',
    # 'Device 8': 'Device_8',
    # 'Device 9': 'Device_9',
    # 'Device 10': 'Device_10',
    # 'Device 11': 'Device_11',
    # 'Device 12': 'Device_12',
    # 'Device 13': 'Device_13',
    # 'Device 14': 'Device_14',
    # 'Device 15': 'Device_15',
    # 'Device 16': 'Device_16',
    # 'Device 17': 'Device_17',
    # 'Device 18': 'Device_18',
    # 'Device 19': 'Device_19',
    # 'Device 20': 'Device_20',
    # 'Sensor 1': 'Sensor_1',
    # 'Sensor 2': 'Sensor_2',
    # 'Sensor 3': 'Sensor_3',
    # 'Sensor 4': 'Sensor_4',
    # 'Sensor 5': 'Sensor_5',
    # 'Sensor 6': 'Sensor_6',
    # 'Sensor 7': 'Sensor_7',
    # 'Sensor 8': 'Sensor_8',
    # 'Sensor 9': 'Sensor_9',
    # 'Sensor 10': 'Sensor_10'
}

def send_telemetry(client, device_token):
    data = {
        'PSGV2': round(random.uniform(1.00,15.00)),
        'RSP2': round(random.uniform(15.50,30.00)),
        'PSP2': round(random.uniform(30.50,45.00)),
        'PHSP2': round(random.uniform(45.50,60.00)),
        'SWP2': round(random.uniform(60.50,75.00)),
        'CWOP2': round(random.uniform(75.50,90.00)),
        'CIT2': round(random.uniform(90.50,105.50)),
        'COT2': round(random.uniform(106.50,120.50))
        # 'temperature': round(random.uniform(20.0, 30.0), 2),
        # 'humidity': round(random.uniform(40.0, 60.0), 2)
    }
    client.publish('v1/devices/me/telemetry', json.dumps(data))

def create_mqtt_client(device_token):
    client = mqtt.Client()
    client.username_pw_set(device_token)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    return client

if __name__ == '__main__':
    clients = {}
    
    for device, token in DEVICE_TOKENS.items():
        clients[device] = create_mqtt_client(token)

    try:
        while True:
            for device, client in clients.items():
                send_telemetry(client, DEVICE_TOKENS[device])
            time.sleep(10)  # Send data every 10 seconds
    except KeyboardInterrupt:
        for client in clients.values():
            client.disconnect()
