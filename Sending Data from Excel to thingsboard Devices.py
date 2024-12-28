import pandas as pd
import paho.mqtt.client as mqtt
import json
import time
import datetime
import warnings

# Suppress the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ThingsBoard Host
THINGSBOARD_HOST = '127.0.0.1'

# Function to read device data from an Excel file
def read_device_data(file_path):
    df = pd.read_excel(file_path)
    return df

def send_telemetry(client, device_name, timestamp, data):
    client.publish(f'v1/devices/me/telemetry', json.dumps(data))

def create_mqtt_client(device_token):
    client = mqtt.Client()
    client.username_pw_set(device_token)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    return client

if __name__ == '__main__':
    # Read device data from Excel file
    device_data = read_device_data('D:/CONTROLYTICS/SIVA_M_WORK/Thingsboard New Folder/Book1.xlsx')
    
    # Create MQTT clients for devices
    clients = {}
    for index, row in device_data.iterrows():
        device_name = row['Device']
        device_token = row['Token']
        clients[device_name] = create_mqtt_client(device_token)
    
    try:
        while True:
            for index, row in device_data.iterrows():
                device_name = row['Device']
                timestamp = row['Timestamp']
                temperature_key = row['Key1']
                temperature_value = row['Value1']
                humidity_key = row['Key2']
                humidity_value = row['Value2']
                
                # Create telemetry data
                data = {
                    temperature_key: temperature_value,
                    humidity_key: humidity_value
                }
                
                # Send telemetry data
                send_telemetry(clients[device_name], device_name, timestamp, data)
            time.sleep(10)  # Send data every 10 seconds
    except KeyboardInterrupt:
        for client in clients.values():
            client.disconnect()
