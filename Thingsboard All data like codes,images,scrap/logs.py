import requests
from datetime import datetime

def get_bearer_token(username, password):
    # Replace with your ThingsBoard login URL
    login_url = 'https://app.controlytics.ai:443/api/auth/login'

    # Set login credentials
    credentials = {
        'username': username,
        'password': password
    }

    # Request a bearer token
    response = requests.post(login_url, json=credentials)

    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Failed to get bearer token. Status code: {response.status_code}")
        return None

def fetch_audit_logs(username, password):
    # Obtain bearer token
    bearer_token = get_bearer_token(username, password)

    if not bearer_token:
        return []

    # Replace with your ThingsBoard URL
    url = 'https://app.controlytics.ai:443/api/audit/logs'
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': f'Bearer {bearer_token}'
    }

    # Sample parameters, modify as needed
    params = {
        'pageSize': 40,  # Number of logs per page
        'page': 5,  # Page number
        # Add other parameters like date range, filters, etc. as needed
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        logs = response.json().get('data', [])

        # Logging the data into the 'data' list
        data = [['Time', 'Entity Type', 'Entity Name', 'User', 'Action Type', 'Status', 'Details']]

        for log in logs:
            formatted_time = datetime.utcfromtimestamp(int(log['createdTime']) // 1000).strftime('%Y-%m-%d %H:%M:%S')
            entity_type = log.get('entityId', {}).get('entityType') if 'entityId' in log else ''
            entity_name = log.get('entityName', '')
            user_name = log.get('userName', '')
            action_type = log.get('actionType', '')
            action_status = log.get('actionStatus', '')
            details = log.get('details', '')

            log_row = [
                formatted_time,
                entity_type,
                entity_name,
                user_name,
                action_type,
                action_status,
                details
            ]
            data.append(log_row)
            print(data)

        return data
    else:
        print(f"Failed to fetch logs. Status code: {response.status_code}")
        return []

# Replace with your ThingsBoard username and password
username = 'team@controlytics.ai'
password = 'controlytics.ai'

# Fetch audit logs and log the data
audit_logs_data = fetch_audit_logs(username, password)

# Now you have the 'audit_logs_data' variable containing the logged data.
# You can use it as needed in the rest of your application.
