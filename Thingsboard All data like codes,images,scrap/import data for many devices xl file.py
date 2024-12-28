import pandas as pd
import requests
import json

def send_to_thingsboard(timestamp, broker_id, access_token, values):
    url = 'http://app.controlytics.ai/api/v1/Sensor_1/telemetry'  # Replace with your ThingsBoard API endpoint
    payload = {
        "ts": timestamp,
        "values": values
    }

    try:
        # Convert the payload dictionary to JSON format
        json_payload = json.dumps(payload)
        print("JSON payload: ", json_payload)

        # Define headers
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, data=json_payload, headers=headers)
        print("response: ", response.content)

        if response.status_code == 200:
            print("Data sent successfully to ThingsBoard!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            # Print response content if needed: print(f"Response content: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

# Read Excel file
excel_file = r'D:\CONTROLYTICS\SIVA_M_WORK\THINGSBOARD\Book1.xlsx'  # Update the file path with 'fork.xlsx'
excel_data = pd.read_excel(excel_file)

for index, row in excel_data.iterrows():
    timestamp = row['timestamp']
    broker_id = row['Broker']
    access_token = row['Token']

    values = {
        row['Key1']: row['Value1'],
        row['Key2']: row['Value2']
        # Add more values if needed following the same pattern
    }
    print(values)
    send_to_thingsboard(timestamp, broker_id, access_token, values)
