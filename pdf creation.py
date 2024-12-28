from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_alarm_report(filename, data):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "GRANULES INDIA LIMITED")
    c.drawCentredString(width / 2, height - 70, "Gagillapur ALARM DATA REPORT")
    
    # Add new fields
    c.setFont("Helvetica", 10)
    c.drawString(30, height - 100, f"Area: {data['area']}")
    c.drawString(30, height - 120, f"Location: {data['location']}")
    c.drawString(30, height - 140, f"Inst ID: {data['inst_id']}")
    c.drawString(30, height - 160, f"Start Date & Time: {data['start_time']}")
    c.drawString(30, height - 180, f"End Date & Time: {data['end_time']}")
    c.drawString(30, height - 200, f"Print Date & Time: {data['print_time']}")
    c.drawString(30, height - 220, f"Reviewed By: {data['reviewed_by']}")
    c.drawString(30, height - 240, f"Comments: {data['comments']}")
    
    # Table Header
    table_header = ["ALARM TYPE", "ALARM CREATED TIME", "ALARM CREATED VALUE", "ALARM SEVERITY", 
                    "ALARM CLEAR TIME", "ALARM CLEARED VALUE", "Acknowledged By", "Acknowledgment Time"]
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.black)
    c.drawString(30, height - 270, " | ".join(table_header))
    
    # Table Data
    c.setFont("Helvetica", 8)
    y_position = height - 290
    for row in data['alarm_data']:
        row_text = " | ".join([str(item) for item in row])
        c.drawString(30, y_position, row_text)
        y_position -= 20
    
    # Footer
    c.drawString(30, 50, f"Printed By: {data['printed_by']}")
    c.drawString(30, 30, f"Printed At: {data['print_time']}")
    
    c.save()

# Example data dictionary
report_data = {
    "area": "Module-F",
    "location": "API Dispensing Booth Area",
    "inst_id": "CWH/RDU/033-00",
    "start_time": "18-10-2024 & 12:00:00",
    "end_time": "18-10-2024 & 12:30:21",
    "print_time": "18-10-2024 & 12:30:42",
    "reviewed_by": "John Doe",
    "comments": "All alarms reviewed.",
    "printed_by": "Admin",
    "alarm_data": [
        ["High Temperature Alarm", "18-10-2024 & 12:01:46", "27.25", "MAJOR", "18-10-2024 & 12:02:32", "25.56", "Jane Smith", "18-10-2024 & 12:05:00"],
        # Add more alarm records here
    ]
}

# Generate the report
generate_alarm_report("extended_alarm_report.pdf", report_data)
