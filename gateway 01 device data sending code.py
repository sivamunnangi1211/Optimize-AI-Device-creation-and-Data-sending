import paho.mqtt.client as mqtt
import json
import random
import time
import warnings

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

THINGSBOARD_HOST = '13.233.112.40'

# Replace these with the access tokens for your devices
DEVICE_TOKENS = {
    'IOTGW03': 'gateway01'
}

def on_publish(client, userdata, mid):
    print(f"Data published with mid: {mid}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnect failed: {e}")

def send_telemetry(client, device_token):
    data = {
        'id': round(random.uniform(101, 115)),
        'ty': round(random.uniform(1, 4))
    }
    
    # Randomly decide how to handle 'v' (actual value, "NA", or omit it)
    v_choice = random.choice(['value'])         #,''
    
    if v_choice == 'value':
        data['v'] = f"{random.uniform(18.00, 30.00):.2f},{random.uniform(40.50, 70.00):.2f}"
    # elif v_choice == 'NA':
    #     data['v'] = "NA,NA"
    
    result = client.publish('v1/devices/me/telemetry', json.dumps(data))
    status = result.rc
    if status == 0:
        print(f"Successfully sent data: {data}")
    else:
        print(f"Failed to send data: {data}")

def create_mqtt_client(device_token):
    client = mqtt.Client()
    client.username_pw_set(device_token)
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.connect(THINGSBOARD_HOST, 1883, keepalive=300)  # Keep the keepalive interval set permanently to 120 seconds
    return client

if __name__ == '__main__':
    clients = {}
    
    for device, token in DEVICE_TOKENS.items():
        clients[device] = create_mqtt_client(token)

    try:
        while True:
            for device, client in clients.items():
                send_telemetry(client, DEVICE_TOKENS[device])
                time.sleep(3)  # 3-second gap between each device
    except KeyboardInterrupt:
        print("Program stopped manually. Disconnecting clients...")
        for client in clients.values():
            client.disconnect()
