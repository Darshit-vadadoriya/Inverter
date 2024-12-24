# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now
from datetime import datetime
    


class AssignMaintenanceSchedule(Document):

    def on_update(self):
       
        for row in self.schedule_assignment:  # Iterate over each row in the child table
            if row.id and row.schedule_date:
                        # Fetch the current schedule_date from Maintenance Schedule Details
                    current_schedule_date = frappe.get_value(
                        "Maintenance Schedule Detail", 
                        {"name": row.id}, 
                        "scheduled_date"
                    )

                    # Only update if the schedule_date has changed
                    if current_schedule_date != row.schedule_date:
                        # Update the schedule_date in the Maintenance Schedule Details table
                        frappe.db.set_value(
                            "Maintenance Schedule Detail",
                            row.id,
                            "scheduled_date",
                            row.schedule_date
                        )

    def on_submit(name):
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

        # Prepare email details and schedules for update
        emails_to_send = []
        schedules_to_update = []

        for schedule in schedule_pending_data:
            frappe.db.set_value("Maintenance Schedule Detail", schedule.id, "custom_technician", schedule.technician)
            frappe.db.set_value("Maintenance Schedule Detail", schedule.id, "custom_technician_email", schedule.email_id)
            if schedule["email"] == 0 and schedule["technician"]:
                # Get technician name and locality
                technician_name = frappe.db.get_value("Employee", schedule.technician, "first_name")
                locality = frappe.db.get_value("Maintenance Schedule", schedule.maintenance_schedule_id, "custom_locality")
                schedule_date = frappe.utils.formatdate(schedule["schedule_date"], "dd-mm-yyyy")

                # Generate email content using a template function
                message = get_email_template(
                    technician=technician_name,
                    item=schedule["item"],
                    schedule_date=schedule_date,
                    assigned_by=frappe.session.user,
                    locality=locality
                )

                # Add email to the queue
                emails_to_send.append({
                    "recipients": schedule["email_id"],
                    "subject": "Maintenance Schedule Assignment",
                    "message": message,
                })

                # Update schedule email status
                schedules_to_update.append(schedule["id"])
                frappe.db.set_value("Maintenance Schedule Detail", schedule.id, "custom_email", 1)
                frappe.db.set_value("Schedule Assign", schedule.name, "email", 1)

        # Enqueue emails for background sending
        if emails_to_send:
            frappe.enqueue(
                send_bulk_emails,
                emails_to_send=emails_to_send,
                timeout=300
            )
            frappe.msgprint("Schedule is assigned.")

        



@frappe.whitelist()
def get_schedules(from_date, to_date):

    # Parse the string inputs into date objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    # Validate date range
    if from_date > to_date:
        frappe.throw("From date cannot be greater than to date.")

    # SQL query to join Maintenance Schedule and Maintenance Schedule Detail
    # and fetch outstanding amount from Sales Invoice
    query = """
        SELECT 
            ms.name AS maintenance_schedule,
            ms.customer,
            ms.custom_locality,
            msd.name,
            msd.item_code,
            msd.custom_technician,
            msd.custom_technician_email,
            msd.custom_email,
            msd.scheduled_date,
            msd.docstatus,
            COALESCE((
                SELECT SUM(si.outstanding_amount)
                FROM `tabSales Invoice` si
                WHERE si.customer = ms.customer
                AND si.docstatus = 1
            ), 0) AS outstanding_amount
        FROM 
            `tabMaintenance Schedule` ms
        RIGHT JOIN 
            `tabMaintenance Schedule Detail` msd ON ms.name = msd.parent
        WHERE 
            msd.scheduled_date BETWEEN %s AND %s
            AND msd.docstatus = 1
            AND (msd.custom_technician = '' OR msd.custom_technician IS NULL)
    """
    
    # Execute the query
    records = frappe.db.sql(query, (from_date, to_date), as_dict=True)
    return records







def send_bulk_emails(emails_to_send):
    """
    Send bulk emails using Frappe's email service.
    """
    for email in emails_to_send:
        frappe.sendmail(
            recipients=email["recipients"],
            subject=email["subject"],
            message=email["message"]
        )
    frappe.email.queue.flush()
    


def get_email_template(technician, item, schedule_date, assigned_by, locality):
    """
    Generate an enhanced and visually appealing HTML email template.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Maintenance Schedule Assignment</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
                color: #333;
            }}
            .container {{
                max-width: 650px;
                margin: 30px auto;
                background: #ffffff;
                border-radius: 15px;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                font-size: 16px;
            }}
            .header {{
                background: linear-gradient(to right, #007BFF, #0056b3);
                padding: 20px;
                text-align: center;
                color: #fff;
            }}
            .header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: bold;
            }}
            .content {{
                padding: 20px 30px;
                line-height: 1.8;
                color: #555;
            }}
            .content ul {{
                list-style: none;
                padding: 0;
                margin: 15px 0;
            }}
            .content ul li {{
                margin-bottom: 10px;
                background: #f8f9fa;
                padding: 12px 15px;
                border-left: 4px solid #007BFF;
                border-radius: 8px;
                font-size: 15px;
                color: #444;
            }}
            .content ul li strong {{
                color: #007BFF;
            }}
            .action-button {{
                display: block;
                text-align: center;
                margin: 30px auto 20px;
                padding: 15px 30px;
                background: #007BFF;
                color: #ffffff;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                width: 60%;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }}
            .action-button:hover {{
                background: #0056b3;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }}
            .footer {{
                background: #f1f1f1;
                text-align: center;
                padding: 15px;
                font-size: 14px;
                color: #777;
                border-top: 1px solid #e0e0e0;
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
                <p>You have been assigned a new maintenance schedule. Below are the details:</p>
                <ul>
                    <li><strong>Item Name:</strong> {item}</li>
                    <li><strong>Scheduled Date:</strong> {schedule_date}</li>
                    <li><strong>Assigned By:</strong> {assigned_by}</li>
                    <li><strong>Area:</strong> {locality}</li>
                </ul>
                <p>Kindly review the schedule and proceed as planned. Should you have any questions, feel free to reach out to the support team.</p>
          
            </div>
          
        </div>
    </body>
    </html>
    """
