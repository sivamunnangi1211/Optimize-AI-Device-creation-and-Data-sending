import requests
import json

THINGSBOARD_URL = "http://app.controlytics.ai"
API_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtQGNvbnRyb2x5dGljcy5haSIsInVzZXJJZCI6IjY2MGU0YmIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiOWZjMWFjYjQtM2U0OS00YWEyLThhYzgtM2RmODZiZmQ2ZWY1IiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MTYxODAxNzIsImV4cCI6MTcxNjI3MDE3MiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjVhNjU4NjIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.Jf31pz9Ar0pFLHvCYhti12RXecpvHzTy_QZXl5nELx6zhFl3oNDdPloVkqN0QmbhCsn_sSXlQPCw7ZXplow75A"

def get_device(device_name):
    url = f"{THINGSBOARD_URL}/api/tenant/devices?deviceName={device_name}"
    headers = {"X-Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            devices = response.json()
            if 'data' in devices and devices['data']:
                return devices['data'][0]['id']['id']
            else:
                print(f"No device found with name: {device_name}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response: {response.text}")
    else:
        print(f"Failed to get device {device_name}. Status code: {response.status_code}, Response: {response.text}")
    return None

def create_device(device_name):
    url = f"{THINGSBOARD_URL}/api/device"
    headers = {"Content-Type": "application/json", "X-Authorization": f"Bearer {API_TOKEN}"}
    payload = {"name": device_name, "type": "default"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['id']['id']
    else:
        print(f"Failed to create device {device_name}. Status code: {response.status_code}, Response: {response.text}")
        return None

def post_telemetry(device_token, data):
    url = f"{THINGSBOARD_URL}/api/v1/{device_token}/telemetry"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Telemetry data posted successfully")
    else:
        print(f"Failed to post telemetry data. Status code: {response.status_code}, Response: {response.text}")

def get_device_token(device_id):
    url = f"{THINGSBOARD_URL}/api/device/{device_id}/credentials"
    headers = {"X-Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['credentialsId']
    else:
        print(f"Failed to get device token. Status code: {response.status_code}, Response: {response.text}")
        return None

def main():
    data_points = [
        {"id": "1", "ty": "temperature", "v": 25},
        {"id": "2", "ty": "humidity", "v": 60},
        {"id": "1", "ty": "temperature", "v": 26}
    ]

    for data in data_points:
        device_name = f"device_{data['id']}"
        device_id = get_device(device_name)

        if not device_id:
            device_id = create_device(device_name)

        if device_id:
            device_token = get_device_token(device_id)
            if device_token:
                telemetry_data = {data['ty']: data['v']}
                post_telemetry(device_token, telemetry_data)

if __name__ == "__main__":
    main()
