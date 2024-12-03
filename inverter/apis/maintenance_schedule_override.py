import frappe
from frappe.utils import today, add_months
from frappe.utils import formatdate
from frappe.utils import add_days, today



# def assign_schedule(doc, method):

#     print(doc.schedules)
#     # Loop through the schedules in the document
#     for i in doc.schedules:
#         # Check if the email has not been sent and a custom technician is assigned
#         if i.custom_email == 0 and i.custom_technician:
#             # Fetch the locality of the maintenance schedule
#             locality = frappe.db.get_value("Maintenance Schedule", i.parent, "custom_locality")
#             print("Done=================")

#             # Create the HTML email message
#             message = """
#                 <html>
#                 <head>
#                     <title>Maintenance Schedule Assignment</title>
#                     <style>
#                         body { font-family: Arial, sans-serif; background-color: #f9f9f9; }
#                         .container { max-width: 600px; margin: auto; padding: 20px; background: #fff; }
#                         .header { text-align: center; margin-bottom: 20px; }
#                         .header h1 { margin: 0; color: #333; }
#                         .content { line-height: 1.6; color: #555; }
#                     </style>
#                 </head>
#                 <body>
#                     <div class="container">
#                         <div class="header">
#                             <h1>Maintenance Schedule Assignment</h1>
#                         </div>
#                         <div class="content">
#                             <p>Dear {custom_technician},</p>
#                             <p>You have been assigned a new maintenance schedule:</p>
#                             <ul>
#                                 <li><strong>Item Name:</strong> {item_code}</li>
#                                 <li><strong>Scheduled Date:</strong> {scheduled_date}</li>
#                                 <li><strong>Assigned By:</strong> {assigned_by}</li>
#                                 <li><strong>Area:</strong> {locality}</li>
#                             </ul>
#                         </div>
#                     </div>
#                 </body>
#                 </html>
#             """.format(
#                 custom_technician=i.custom_technician,
#                 item_code=i.item_code,
#                 scheduled_date=i.scheduled_date,
#                 assigned_by=frappe.session.user,
#                 locality=locality
#             )
#             # Send the email to the technician
#             frappe.sendmail(
#                 recipients=i.custom_technician_email,
#                 subject=frappe._('Maintenance Schedule Assignment'),
#                 message=message
#             )

#             # Update the custom_email field to indicate the email has been sent
#             frappe.db.set_value("Maintenance Schedule Detail", i.name, "custom_email", 1)

            
#     frappe.email.queue.flush()

# ============================================================================ It is work Slow
# def assign_schedule(doc, method):
#     for i in doc.schedules:
#         print(f"Processing Schedule Detail: {i.name}")
#         if i.custom_email == 0 and i.custom_technician:
#             locality = frappe.db.get_value("Maintenance Schedule", i.parent, "custom_locality")
#             technician = frappe.db.get_value("Employee", i.custom_technician, "first_name")
#             schedule_date = formatdate(i.scheduled_date, "dd-mm-yyyy")
    

#             # Create the email content
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
#                                 <li><strong>Item Name:</strong> {i.item_code}</li>
#                                 <li><strong>Scheduled Date:</strong> {schedule_date}</li>
#                                 <li><strong>Assigned By:</strong> {frappe.session.user}</li>
#                                 <li><strong>Area:</strong> {locality}</li>
#                             </ul>technician_names
#                             <p>Ensure to complete the maintenance as scheduled. For further assistance, contact the support team.</p>
#                         </div>
#                         <div class="footer">
#                             <p>This email was generated automatically by the Maintenance Management System.</p>
#                         </div>
#                     </div>
#                 </body>
#                 </html>
#             """

        
        
#             # Send the email
#             frappe.sendmail(
#                 recipients=i.custom_technician_email,
#                 subject="Maintenance Schedule Assignment",
#                 message=message,
#             )
#             frappe.db.set_value("Maintenance Schedule Detail",i.name,"custom_email",1)
#             frappe.email.queue.flush()


def assign_schedule(doc, method):
        # Fetch all necessary data using frappe.get_list without as_dict
        technician_data = frappe.get_list("Employee", 
            fields=["name", "first_name"], filters={"name": ["in", [i.custom_technician for i in doc.schedules]]})
        
        locality_data = frappe.get_list("Maintenance Schedule", 
            fields=["name", "custom_locality"], filters={"name": ["in", [i.parent for i in doc.schedules]]})

        # Convert the fetched data to dictionaries for fast lookups
        technician_names = {t["name"]: t["first_name"] for t in technician_data}
        localities = {l["name"]: l["custom_locality"] for l in locality_data}

        # Prepare lists to store email details and schedules for update
        emails_to_send = []
        schedules_to_update = []

        # Loop through schedules and prepare email details
        for i in doc.schedules:
            if i.custom_email == 0 and i.custom_technician:
                technician = technician_names.get(i.custom_technician, "")
                locality = localities.get(i.parent, "")
                schedule_date = formatdate(i.scheduled_date, "dd-mm-yyyy")

                # Create email content
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
                                    <li><strong>Item Name:</strong> {i.item_code}</li>
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

                # Add email details to the list
                emails_to_send.append({
                    "recipients": i.custom_technician_email,
                    "subject": "Maintenance Schedule Assignment",
                    "message": message,
                })

                # Mark the schedule to indicate the email has been sent
                schedules_to_update.append(i)

        # Batch update the schedules (using ORM)
        if schedules_to_update:
            for schedule in schedules_to_update:
                schedule.custom_email = 1
                schedule.save()

        # Enqueue email sending in the background
        if emails_to_send:
            # Use frappe.enqueue to send emails in the background
            frappe.enqueue(
                send_bulk_emails,
                emails_to_send=emails_to_send,
                timeout=300  # Adjust the timeout as needed
            )

# Function to send emails in the background
def send_bulk_emails(emails_to_send):
    for email in emails_to_send:
        frappe.sendmail(
            recipients=email["recipients"],
            subject=email["subject"],
            message=email["message"]
        )
    
    # Flush the email queue to send emails immediately
    frappe.email.queue.flush()


# @frappe.whitelist()
# def schedule_reminder():
#     email_ids = frappe.db.sql(
# 			"SELECT email_id FROM `tabEmail Recipients` WHERE parent='Support Setup'", as_dict=1
# 		)
#     email_list = [item["email_id"] for item in email_ids]
    
#     days = frappe.db.get_single_value("Support Setup","schedule_reminder")
#     reminder_date = add_days(today(), -int(days))  # Calculate the date 15 days from today
#     records = frappe.db.get_all(
#         "Maintenance Schedule Detail",
#         fields=["*"],
#         filters={
#             "completion_status": "Pending",
#             "scheduled_date": ["<=", reminder_date],  # Schedule date within the next 15 days
#         }
#     )   
    
#      # If no records, return or log a message
#     if records:
        
#         # Create HTML table from records
#         table_html = """
#         <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
#             <thead>
#                 <tr>
#                     <th>Parent</th>
#                     <th>Item Name</th>
#                     <th>Scheduled Date</th>
#                 </tr>
#             </thead>
#             <tbody>
#         """
        
#         for record in records:
#             table_html += f"""
#                 <tr>
#                     <td>{record.parent}</td>
#                     <td>{record.item_name}</td>
#                     <td>{record.scheduled_date}</td>
#                 </tr>
#             """
        
#         table_html += """
#             </tbody>
#         </table>
#         """
        
     
        
#         subject = "Pending Maintenance Schedules Reminder"
#         message = f"""
#         <p>Dear Admin,</p>
#         <p>Below are the pending maintenance schedules that need attention:</p>
#         {table_html}
       
#         """
        
#         frappe.sendmail(
#             recipients=email_list,
#             subject=subject,
#             message=message,
#             header="Reminder: Pending Maintenance Schedules"
#         )
#         frappe.email.queue.flush()




import frappe
from frappe.utils import add_days, today

@frappe.whitelist()
def schedule_reminder():
    # Fetch email addresses
    email_ids = frappe.db.sql(
        "SELECT email_id FROM `tabEmail Recipients` WHERE parent='Support Setup'", as_dict=1
    )
    email_list = [item["email_id"] for item in email_ids]
    
    # Get reminder days from setup
    days = frappe.db.get_single_value("Support Setup", "schedule_reminder")
    reminder_date = add_days(today(), -int(days))  # Calculate the reminder date
    
    # Fetch pending maintenance records that are submitted (docstatus = 1)
    records = frappe.db.get_all(
        "Maintenance Schedule Detail",
        fields=["parent", "item_name", "scheduled_date"],
        filters={
            "completion_status": "Pending",
            "scheduled_date": ["<=", reminder_date],  # Schedule date within the next X days
            "docstatus": 1  # Only submitted maintenance schedules
        }
    )
    
    # If no records, log a message and stop execution
    if not records:
        frappe.msgprint("No pending maintenance schedules found.")
        return
    
    # Create HTML table with improved design and clickable links
    table_html = """
    <table style="width: 100%; border: 1px solid #e0e0e0; border-collapse: collapse; font-family: Arial, sans-serif; text-align: left; margin-top: 20px;">
        <thead style="background-color: #4CAF50; color: white;">
            <tr>
                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Maintenance Schedule</th>
                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Item Name</th>
                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Scheduled Date</th>
            </tr>
        </thead>
        <tbody style="background-color: #f9f9f9;">
    """
    
    # Loop through the records to populate the table rows
    for record in records:
        schedule_date = frappe.utils.formatdate(record.scheduled_date, "dd-MM-yyyy")
        maintenance_schedule_link = f'<a href="/app/maintenance-schedule/{record.parent}" target="_blank" style="color: black; text-decoration: underline;">{record.parent}</a>'
        table_html += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #333;">{maintenance_schedule_link}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #333;">{record.item_name}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #333;">{schedule_date}</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """
    
    # Email Subject and Message
    subject = "Reminder: Pending Maintenance Schedules"
    message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #555;">
            <div style="background-color: #f7f7f7; padding: 20px; border-radius: 5px;">
                <h3 style="color: #333; font-weight: bold;">Dear Sir/Medam,</h3>
                
                <p style="font-size: 16px; color: #333;">We are sending this reminder regarding the following <strong>pending maintenance schedules</strong> that require your attention. Please review the details below:</p>
                
                {table_html}
                
             
                <hr style="border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="font-size: 14px; color: #999;">This is an automated reminder. Please do not reply to this email.</p>
            </div>
        </body>
    </html>
    """
    
    # Send email
    try:
        frappe.sendmail(
            recipients=email_list,
            subject=subject,
            message=message,
            header="Reminder: Pending Maintenance Schedules"
        )
        frappe.email.queue.flush()
        frappe.msgprint("Reminder email sent successfully.")
    except Exception as e:
        frappe.log_error(f"Error sending email: {str(e)}", "Schedule Reminder Email Error")
        frappe.msgprint(f"Error sending email: {str(e)}")
