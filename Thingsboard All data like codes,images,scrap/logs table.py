from reportlab.lib.pagesizes import letter
import requests
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

# Function to fetch ThingsBoard audit logs
def fetch_audit_logs():
    # Replace with your ThingsBoard URL and access token
    url = 'https://app.controlytics.ai:443/api/audit/logs'
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtQGNvbnRyb2x5dGljcy5haSIsInVzZXJJZCI6IjY2MGU0YmIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiOGIxNzBmMjQtMTkwYS00MGVmLTkxYWItZjFhMjc0ZDQ0OGNjIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDU0NzAxMDUsImV4cCI6MTcwNTQ3OTEwNSwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjVhNjU4NjIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ._30dkLD-AtzttZmkVjK9PSxFLO0UDHpJVdmqHqfOudrODi9ljyXLdn-4eD2H2m61KCEAklm2IT9PpzFon9z89g'   }

    # Sample parameters, modify as needed
    params = {
        'pageSize': 40,  # Number of logs per page
        'page': 5,  # Page number
        # Add other parameters like date range, filters, etc. as needed
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        #print(response.json())
        return response.json()['data']
    else:
        print(f"Failed to fetch logs. Status code: {response.status_code}")
        return []

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
            log.get('entityName',''),
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

        table = Table(table_data)
        table.setStyle(style)
        elements.append(table)

    doc.build(elements)
    print(f"PDF generated: {pdf_filename}")





# Fetch audit logs
audit_logs = fetch_audit_logs()

# Create PDF in table format
create_pdf(audit_logs)
