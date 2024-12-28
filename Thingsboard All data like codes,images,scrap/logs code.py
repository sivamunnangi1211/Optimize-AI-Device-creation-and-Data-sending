import requests

# Define the URL and bearer token
url = 'https://app.controlytics.ai:443/api/audit/logs'
bearer_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtQGNvbnRyb2x5dGljcy5haSIsInVzZXJJZCI6IjY2MGU0YmIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiOGIxNzBmMjQtMTkwYS00MGVmLTkxYWItZjFhMjc0ZDQ0OGNjIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDU0NzAxMDUsImV4cCI6MTcwNTQ3OTEwNSwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjVhNjU4NjIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ._30dkLD-AtzttZmkVjK9PSxFLO0UDHpJVdmqHqfOudrODi9ljyXLdn-4eD2H2m61KCEAklm2IT9PpzFon9z89g'
# Define headers with bearer token


headers = {
    'Content-Type': 'application/json',
    'X-Authorization': f'Bearer {bearer_token}'
}

params = {
        'pageSize': 40,  # Number of logs per page
        'page': 1,  # Page number
        # Add other parameters like date range, filters, etc. as needed
    }

try:
    # Make a GET request to fetch JSON data
    response = requests.get(url, headers=headers,params=params)

    if response.status_code == 200:
        # Extract JSON data from the response
        json_data = response.json()

        # Extracting specific fields
        created_time = json_data.get('createdTime')
        tenant_entity_type = json_data.get('tenantId', {}).get('entityType')
        customer_entity_type = json_data.get('customerId', {}).get('entityType')
        entity_id_type = json_data.get('entityId', {}).get('entityType')
        entity_name = json_data.get('entityName')
        user_entity_type = json_data.get('userId', {}).get('entityType')
        user_name = json_data.get('userName')
        action_type = json_data.get('actionType')
        action_data = json_data.get('actionData')
        action_status = json_data.get('actionStatus')

        # Displaying extracted fields
        print("createdTime:", created_time)
        print("tenantId['entityType']:", tenant_entity_type)
        print("customerId['entityType']:", customer_entity_type)
        print("entityId['entityType']:", entity_id_type)
        print("entityName:", entity_name)
        print("userId['entityType']:", user_entity_type)
        print("userName:", user_name)
        print("actionType:", action_type)
        print("actionData:", action_data)
        print("actionStatus:", action_status)
        print("JSON Response:", response.json())

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Text:", response.text)  # Print response text for error details

except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)