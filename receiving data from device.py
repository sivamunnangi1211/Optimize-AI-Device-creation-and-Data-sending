import requests
import json

# Define ThingsBoard API endpoint for fetching telemetry data
api_url = "https://app.controlytics.ai:443/api/v1/gateway01/attributes"

# Define the access token or authentication credentials
access_token = "gateway01"

# Define request headers
headers = {
    "Content-Type": "application/json",
    "X-Authorization": f"Bearer {access_token}"
}

# Debug: Print headers for verification
print("Request Headers:", headers)

# Send HTTP GET request to fetch telemetry data
response = requests.get(api_url, headers=headers)

# Debug: Print response status code
print("Response Status Code:", response.status_code)

# Check response status
if response.status_code == 200:
    # Parse the response JSON
    telemetry_data = response.json()
    print("Telemetry data retrieved successfully:", telemetry_data)
else:
    print("Failed to fetch telemetry data. Status code:", response.status_code)
