import requests
import json
import random

# ThingsBoard device access tokens
MAIN_FLOW_METER_TOKEN = "mainflow"
SUB_FLOW_METER_1_TOKEN = "flowmeter01"
SUB_FLOW_METER_2_TOKEN = "flowmeter02"
SUB_FLOW_METER_3_TOKEN = "flowmeter03"

# ThingsBoard API URL
BASE_URL = "http://app.controlytics.ai:8080/api/v1"

# Function to send telemetry data to ThingsBoard
def send_telemetry(device_token, telemetry_data):
    url = f"{BASE_URL}/{device_token}/telemetry"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(telemetry_data))
    if response.status_code == 200:
        print(f"Data sent successfully to device with token {device_token}: {telemetry_data}")
    else:
        print(f"Failed to send data: {response.status_code} {response.text}")

# Main flow meter telemetry value
main_flow_rate = 50  # Example main flow rate

# Divide flow rate into three equal parts
divided_flow_rate = main_flow_rate / 3

# Randomly adjust one of the sub flow meter values
random_meter = random.choice(["sub1", "sub2", "sub3"])
adjustment = random.uniform(-5, 5)  # Random adjustment value
adjusted_value = divided_flow_rate + adjustment if random_meter == "sub1" else divided_flow_rate

# Prepare telemetry data
telemetry_data = {
    "main_flow_rate": main_flow_rate,
    "sub_flow_rate_1": divided_flow_rate if random_meter != "sub1" else adjusted_value,
    "sub_flow_rate_2": divided_flow_rate if random_meter != "sub2" else adjusted_value,
    "sub_flow_rate_3": divided_flow_rate if random_meter != "sub3" else adjusted_value,
}

# Send telemetry data
send_telemetry(MAIN_FLOW_METER_TOKEN, {"main_flow_rate": main_flow_rate})
send_telemetry(SUB_FLOW_METER_1_TOKEN, {"sub_flow_rate": telemetry_data["sub_flow_rate_1"]})
send_telemetry(SUB_FLOW_METER_2_TOKEN, {"sub_flow_rate": telemetry_data["sub_flow_rate_2"]})
send_telemetry(SUB_FLOW_METER_3_TOKEN, {"sub_flow_rate": telemetry_data["sub_flow_rate_3"]})
