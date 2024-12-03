# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssignMaintenanceSchedule(Document):
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


# @frappe.whitelist()
# def assign_schedule(name):
#     # Fetch pending schedule data
#     schedule_pending_data = frappe.db.get_all(
#         "Schedule Assign",
#         fields=["*"],
#         filters={
#             "parent": name,
#             "email": 0,
#             "technician": ["!=", ""]
#         }
#     )

#     # Update custom technician and email fields
#     for i in schedule_pending_data:
#         frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_technician", i.technician)
#         frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_technician_email", i.email_id)

  
#     # Prepare email details and schedules for update
#     emails_to_send = []
#     schedules_to_update = []

#     for i in schedule_pending_data:
#         if i["email"] == 0 and i["technician"]:
#             technician = frappe.db.get_value("Employee",i.technician,"first_name")
#             locality = frappe.db.get_value("Maintenance Schedule",i.maintenance_schedule_id,"custom_locality")
#             schedule_date = frappe.utils.formatdate(i["schedule_date"], "dd-mm-yyyy")

#             # Email content
#             message = f"""
#                 <!DOCTYPE html>
#                 <html lang="en">
#                 <head>
#                     <meta charset="UTF-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                     <title>Maintenance Schedule Assignment</title>
#                     <style>
#                         body {{
#                             font-family: Arial, sans-serif;
#                             background-color: #f4f4f4;
#                             margin: 0;
#                             padding: 0;
#                             line-height: 1.6;
#                         }}
#                         .container {{
#                             max-width: 600px;
#                             margin: 20px auto;
#                             background: #ffffff;
#                             padding: 20px;
#                             border-radius: 8px;
#                             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#                         }}
#                         .header {{
#                             text-align: center;
#                             margin-bottom: 20px;
#                         }}
#                         .header h1 {{
#                             color: #333333;
#                             margin: 0;
#                             font-size: 24px;
#                         }}
#                         .content {{
#                             color: #555555;
#                             font-size: 16px;
#                         }}
#                         .content ul {{
#                             padding-left: 20px;
#                         }}
#                         .content ul li {{
#                             margin-bottom: 10px;
#                         }}
#                         .footer {{
#                             margin-top: 20px;
#                             text-align: center;
#                             font-size: 12px;
#                             color: #888888;
#                         }}
#                     </style>
#                 </head>
#                 <body>
#                     <div class="container">
#                         <div class="header">
#                             <h1>Maintenance Schedule Assignment</h1>
#                         </div>
#                         <div class="content">
#                             <p>Dear {technician},</p>
#                             <p>You have been assigned a new maintenance schedule. Please find the details below:</p>
#                             <ul>
#                                 <li><strong>Item Name:</strong> {i['item']}</li>
#                                 <li><strong>Scheduled Date:</strong> {schedule_date}</li>
#                                 <li><strong>Assigned By:</strong> {frappe.session.user}</li>
#                                 <li><strong>Area:</strong> {locality}</li>
#                             </ul>
#                             <p>Ensure to complete the maintenance as scheduled. For further assistance, contact the support team.</p>
#                         </div>
#                         <div class="footer">
#                             <p>This email was generated automatically by the Maintenance Management System.</p>
#                         </div>
#                     </div>
#                 </body>
#                 </html>
#             """

#             # Add email to the queue
#             emails_to_send.append({
#                 "recipients": i["email_id"],
#                 "subject": "Maintenance Schedule Assignment",
#                 "message": message,
#             })

#             # Update schedule email status
#             schedules_to_update.append(i["id"])
#             frappe.db.set_value("Maintenance Schedule Detail", i.id, "custom_email", 1)
#             frappe.db.set_value("Schedule Assign", i.name, "email", 1)


#     # Enqueue emails for background sending
#     if emails_to_send:
#         frappe.enqueue(
#             send_bulk_emails,
#             emails_to_send=emails_to_send,
#             timeout=300
#         )


# def send_bulk_emails(emails_to_send):
#     for email in emails_to_send:
#         frappe.sendmail(
#             recipients=email["recipients"],
#             subject=email["subject"],
#             message=email["message"]
#         )
#     frappe.email.queue.flush()


      




@frappe.whitelist()
def assign_schedule(name):
    """
    Assign maintenance schedules to technicians, update records,
    and send notification emails using a user-friendly template.
    """

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
