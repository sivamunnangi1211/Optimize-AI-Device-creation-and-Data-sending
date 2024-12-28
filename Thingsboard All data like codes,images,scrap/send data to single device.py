import pandas as pd
import requests
import json

# Thingsboard server details
tb_server = 'http://app.controlytics.ai:8080'
tb_token = 'Device_1'

FilePath = r"C:\Users\Pavankumar\Desktop\thingsboard\fork.xlsx"
print(FilePath)
xls = pd.ExcelFile(FilePath)

def main():
    for sheet_name in xls.sheet_names:
        print(sheet_name)
        df = pd.read_excel(FilePath, sheet_name=sheet_name)
        rows = df.shape[0]
        for i in range(rows):
            data = {
                "key1": int(df['timestamp'][i]),
                str(df['Key1'][i]): str(df['Value1'][i]),
                str(df['Key2'][i]): str(df['Value2'][i]),
                str(df['Key3'][i]): str(df['Value3'][i]),
                str(df['Key4'][i]): str(df['Value4'][i]),
                str(df['Key5'][i]): str(df['Value5'][i]),
                str(df['Key6'][i]): str(df['Value6'][i])
            }
            print(data)
            topic = df['Topic'][i]
            print(topic)
            
            # Convert data to JSON format
            payload = json.dumps(data)
            
            # Set the request headers
            headers = {
                'Content-Type': 'application/json',
                'X-Authorization': 'Bearer ' + tb_token
            }
            
            # Send POST request to Thingsboard server
            url = f"{tb_server}/api/v1/{tb_token}/telemetry"  # Use 'topic' instead of 'tb_token' here
            response = requests.post(url, data=payload, headers=headers)
            
            # Check response status
            if response.status_code == 200:
                print(f"Data added successfully! Sheet: {sheet_name}, Row: {i}")
            else:
                print(f"Failed to add data. Status code: {response.status_code}")

main()
