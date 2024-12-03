# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import formatdate
from frappe.model.document import Document


class MaintenanceScheduleAssignment(Document):
	pass

@frappe.whitelist()
def get_schedules(from_date, to_date):
    from datetime import datetime

    # Parse the string inputs into date objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    query = """
		SELECT * 
		FROM `tabMaintenance Schedule Detail`
		WHERE scheduled_date BETWEEN %s AND %s 
		AND docstatus = 1 
		AND (custom_technician = '' OR custom_technician IS NULL)
	"""

    
    # Execute the query
    records = frappe.db.sql(query, (from_date, to_date), as_dict=True)
    
    return records


@frappe.whitelist()
def assign_schedule(name):
    # Fetch pending schedule data
    schedule_pending_data = frappe.db.get_all(
        "Schedule Assign",
        fields=["*"],
        filters={
            "parent": name,
            "email": 0,
            "technician": ["!=", ""]
        }
    )

    # Update custom technician and email fields
    for i in schedule_pending_data:
        frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_technician", i.technician)
        frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_technician_email", i.email_id)

  
    # Prepare email details and schedules for update
    emails_to_send = []
    schedules_to_update = []

    for i in schedule_pending_data:
        if i["email"] == 0 and i["technician"]:
            technician = frappe.db.get_value("Employee",i.technician,"first_name")
            locality = frappe.db.get_value("Maintenance Schedule",i.maintenance_schedule_id,"custom_locality")
            schedule_date = formatdate(i["schedule_date"], "dd-mm-yyyy")

            # Email content
            message = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Maintenance Schedule Assignment</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            line-height: 1.6;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            background: #ffffff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        }}
                        .header {{
                            text-align: center;
                            margin-bottom: 20px;
                        }}
                        .header h1 {{
                            color: #333333;
                            margin: 0;
                            font-size: 24px;
                        }}
                        .content {{
                            color: #555555;
                            font-size: 16px;
                        }}
                        .content ul {{
                            padding-left: 20px;
                        }}
                        .content ul li {{
                            margin-bottom: 10px;
                        }}
                        .footer {{
                            margin-top: 20px;
                            text-align: center;
                            font-size: 12px;
                            color: #888888;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Maintenance Schedule Assignment</h1>
                        </div>
                        <div class="content">
                            <p>Dear {technician},</p>
                            <p>You have been assigned a new maintenance schedule. Please find the details below:</p>
                            <ul>
                                <li><strong>Item Name:</strong> {i['item']}</li>
                                <li><strong>Scheduled Date:</strong> {schedule_date}</li>
                                <li><strong>Assigned By:</strong> {frappe.session.user}</li>
                                <li><strong>Area:</strong> {locality}</li>
                            </ul>
                            <p>Ensure to complete the maintenance as scheduled. For further assistance, contact the support team.</p>
                        </div>
                        <div class="footer">
                            <p>This email was generated automatically by the Maintenance Management System.</p>
                        </div>
                    </div>
                </body>
                </html>
            """

            # Add email to the queue
            emails_to_send.append({
                "recipients": i["email_id"],
                "subject": "Maintenance Schedule Assignment",
                "message": message,
            })

            # Update schedule email status
            schedules_to_update.append(i["id"])
            frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_email", 1)
            frappe.db.set_value("Schedule Assign", i.name, "email", 1)


    # Enqueue emails for background sending
    if emails_to_send:
        frappe.enqueue(
            send_bulk_emails,
            emails_to_send=emails_to_send
        )

       # Success message
    frappe.msgprint("Maintenance schedules successfully assigned and emails sent.")


def send_bulk_emails(emails_to_send):
    for email in emails_to_send:
        frappe.sendmail(
            recipients=email["recipients"],
            subject=email["subject"],
            message=email["message"]
        )
    frappe.email.queue.flush()


