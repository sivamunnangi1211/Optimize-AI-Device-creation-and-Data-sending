import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

# Function to fetch ThingsBoard audit logs
def fetch_audit_logs():
    # Replace with your ThingsBoard URL and access token
    url = 'https://app.controlytics.ai:443/api/audit/logs'
    headers = {
        'Content-Type': 'application/json',
        'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtQGNvbnRyb2x5dGljcy5haSIsInVzZXJJZCI6IjY2MGU0YmIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiOGIxNzBmMjQtMTkwYS00MGVmLTkxYWItZjFhMjc0ZDQ0OGNjIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDU0NzAxMDUsImV4cCI6MTcwNTQ3OTEwNSwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjVhNjU4NjIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ._30dkLD-AtzttZmkVjK9PSxFLO0UDHpJVdmqHqfOudrODi9ljyXLdn-4eD2H2m61KCEAklm2IT9PpzFon9z89g'
    }

    # Sample parameters, modify as needed
    params = {
        'pageSize': 40,  # Number of logs per page
        'page': 1,  # Page number
        # Add other parameters like date range, filters, etc. as needed
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to fetch logs. Status code: {response.status_code}")
        return []

# Function to create a PDF from audit logs
def create_pdf(logs):
    pdf_filename = 'C:/logs/audit_logs.pdf'  # Specify your desired path here
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, 'ThingsBoard Audit Logs')

    table_data = [
        ['Time', 'Entity Type', 'Entity Name', 'User', 'Action Type', 'Status', 'Details']
    ]

    for log in logs:
        log_row = [
            log['createdTime'],
            log.get('entityType', ''),
            log.get('entityName', ''),
            log.get('userName', ''),
            log['actionType'],
            log.get('actionStatus', ''),
            log.get('Details', '')
        ]
        table_data.append(log_row)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Gridlines
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Border around table
    ])

    table = Table(table_data)
    table.setStyle(style)

    table.wrapOn(c, 400, 600)
    table.drawOn(c, 100, 650)

    c.save()
    print(f"PDF generated: {pdf_filename}")

# Fetch audit logs
audit_logs = fetch_audit_logs()

# Create PDF
create_pdf(audit_logs)
