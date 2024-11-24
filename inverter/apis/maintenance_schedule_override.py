import frappe
from frappe.utils import today, add_months
from frappe.utils import formatdate


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


def assign_schedule(doc, method):
    for i in doc.schedules:
        print(f"Processing Schedule Detail: {i.name}")
        if i.custom_email == 0 and i.custom_technician:
            locality = frappe.db.get_value("Maintenance Schedule", i.parent, "custom_locality")
            technician = frappe.db.get_value("Employee", i.custom_technician, "first_name")
            schedule_date = formatdate(i.scheduled_date, "dd-mm-yyyy")
    

            # Create the email content
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

        
        
            # Send the email
            frappe.sendmail(
                recipients=i.custom_technician_email,
                subject="Maintenance Schedule Assignment",
                message=message,
            )
            frappe.db.set_value("Maintenance Schedule Detail",i.name,"custom_email",1)
            frappe.email.queue.flush()
