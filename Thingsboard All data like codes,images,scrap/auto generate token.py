from reportlab.lib.pagesizes import letter
import requests
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

# Function to generate ThingsBoard Bearer Token
def get_access_token(base_url, username, password):
    login_url = f"{base_url}/api/auth/login"
    credentials = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(login_url, json=credentials)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get("token")

        if access_token:
            print("Bearer Token:", access_token)
            return access_token
        else:
            print("Error: Unable to obtain Bearer Token")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to fetch ThingsBoard audit logs
def fetch_audit_logs(base_url, username, password):
    access_token = get_access_token(base_url, username, password)

    if not access_token:
        return []

    url = f"{base_url}/api/audit/logs"
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': f'Bearer {access_token}'
    }

    params = {
        'pageSize': 40,
        'page': 3,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data']

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch logs. Status code: {response.status_code}")
        return []

# Function to create a PDF from audit logs in table format
# Function to create a PDF from audit logs in table format
# Function to create a PDF from audit logs in table format
def create_pdf(logs):
    pdf_filename = 'C:/logs/audit_logs.pdf'

    # Define table headers
    table_headers = ['Time', 'Entity Type', 'Entity Name', 'User', 'Action Type', 'Status', 'Details']

    # Organize data into a list of lists for table creation
    data = [table_headers]  # Initial data with headers

    for log in logs:
        formatted_time = datetime.utcfromtimestamp(int(log['createdTime']) // 1000).strftime('%Y-%m-%d %H:%M:%S')
        log_row = [
            formatted_time,
            log.get('entityId', {}).get('entityType'),
            log.get('entityName', ''),
            log.get('userName', ''),
            log['actionType'],
            log.get('actionStatus', ''),
            log.get('details', '')
        ]
        data.append(log_row)

    # Define table style with smaller font size
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Adjust font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Adjust padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Header line
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Header line
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),  # Vertical lines
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),  # Vertical lines
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
    ])

    # Calculate table height considering 18 units per row and extra 18 units for headers
    row_height = 18
    table_height = (len(data) + 1) * row_height

    # Initialize the PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    # Add tables to the document
    while data:
        table_data = data[:38]  # Limit rows per page
        data = data[38:]

        # Calculate row heights for each page
        row_heights = [row_height] * len(table_data)

        table = Table(table_data, rowHeights=row_heights)
        table.setStyle(style)
        elements.append(table)

    doc.build(elements)
    print(f"PDF generated: {pdf_filename}")


# ThingsBoard server details
thingsboard_url = "https://app.controlytics.ai:443"  # Replace with your ThingsBoard instance URL
username = "pavan@controlytics.io"
password = "CAI@buy@1"

# Fetch audit logs
audit_logs = fetch_audit_logs(thingsboard_url, username, password)

# Create PDF in table format
create_pdf(audit_logs)
