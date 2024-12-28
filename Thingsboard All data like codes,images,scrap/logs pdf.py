import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    
def get_entity_type(log):
    entity_id = log.get('entityId', {})
    return entity_id.get('entityType', '')

# Function to create a PDF from audit logs
def create_pdf(logs):
    pdf_filename = 'C:/logs/audit_logs.pdf'  # Specify your desired path here
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, 'ThingsBoard Audit Logs')

    y_start = 700  # Starting y-coordinate for logs (adjusted for more space)
    y_offset = y_start

    line_height = 15  # Height of each line
    available_space = y_start - 50  # Available space on the page

    for log in logs:
        log_text = f"Time: {log['createdTime']}\nEntity Type: {get_entity_type(log)}\nEntity Name: {log.get('entityName')}\nUser: {log.get('userName')}\nAction Type: {log['actionType']}\nStatus: {log.get('actionStatus')}\nDetails: {log.get('Details')}"

        lines = log_text.split('\n')

        # Calculate total height needed for this log entry
        total_height = len(lines) * line_height

        if total_height > available_space:
            c.showPage()  # Create a new page
            c.drawString(100, 750, 'ThingsBoard Audit Logs')
            y_offset = y_start  # Reset y-coordinate for new page
            available_space = y_start - 50  # Reset available space

        for line in lines:
            c.drawString(100, y_offset, line)
            y_offset -= line_height
            available_space -= line_height

        y_offset -= 10  # Add some extra space between log entries

 
    c.save()
    print(f"PDF generated: {pdf_filename}")

# Fetch audit logs
audit_logs = fetch_audit_logs()

# Create PDF
create_pdf(audit_logs)
   
