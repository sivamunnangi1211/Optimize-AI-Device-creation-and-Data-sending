import requests
import json
import openpyxl
import time

# ThingsBoard server details
THINGSBOARD_HOST = '13.234.60.181'  # Replace with your ThingsBoard host
DEVICE_PROFILE_ACCESS_TOKEN = '6bf8ec30-1294-11ef-9ff6-ad6c50e20b96'  # Replace with your device profile access token

# Function to send telemetry data to ThingsBoard
def send_telemetry(device_name, temperature, humidity):
    url = f'http://{THINGSBOARD_HOST}/api/v1/{DEVICE_PROFILE_ACCESS_TOKEN}/telemetry'
    headers = {'Content-Type': 'application/json'}
    payload = {'ts': int(time.time() * 1000), 'values': {'temperature': temperature, 'humidity': humidity}}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f'Telemetry data sent successfully to {device_name}')
    else:
        print(f'Failed to send telemetry data to {device_name}. Status code: {response.status_code}')

# Read data from Excel file
def read_excel(filename):
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active
    for row in sheet.iter_rows(min_row=2, values_only=True):
        device_name, temperature, humidity = row
        send_telemetry(device_name, temperature, humidity)
        time.sleep(1)

if __name__ == '__main__':
    excel_file = 'devices_data.xlsx'  # Replace with your Excel file name
    read_excel(excel_file)
