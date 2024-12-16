import frappe
from frappe.utils import get_url
from frappe.utils import flt


def send_purchase_order_email(doc, method):
    supplier_email = frappe.get_value("Supplier",doc.supplier,["email_id"],as_dict=1)
    print(supplier_email)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # Fetching shipping address details if available
    ship_addr = {}
    if doc.shipping_address:
        ship_addr = frappe.db.get_value(
            "Address",
            doc.shipping_address,
            ["address_line1", "address_line2", "city", "state", "pincode"],
            as_dict=True
        ) or {}

    # Assuming ship_addr is a dictionary-like object
    address_parts = []

    # Add address line 1 if available
    if ship_addr.get("address_line1"):
        address_parts.append(ship_addr["address_line1"])

    # Add address line 2 if available
    if ship_addr.get("address_line2"):
        address_parts.append(ship_addr["address_line2"])

    # Add city if available
    if ship_addr.get("city"):
        address_parts.append(ship_addr["city"])

    # Add state if available
    if ship_addr.get("state"):
        address_parts.append(ship_addr["state"])

    # Add pincode if available
    if ship_addr.get("pincode"):
        address_parts.append(ship_addr["pincode"])

    # Join all parts with commas and a space
    address = ", ".join(address_parts)

    # Get the logo URL with the base URL
    logo_url = get_url() + "/files/logo.png"

    # Constructing the HTML with inline styles
    html = f"""

    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Purchase Order</title>
      <style>
        .taxes thead tr {{
          background-color: #d8d8d8;
          color: #000;
        }}
        .taxes th {{
          padding: 10px;
          border: 1px solid #000;
          text-align: center;
        }}
        .taxes td {{
          padding: 10px;
          border: 1px solid #000;
          text-align: center;
        }}
      </style>
    </head>
    <body style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; line-height: 1.6;">
      <div style="min-width: 700px;max-width:850px;border:1px solid #dfdfdf; margin: 30px auto; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); overflow: hidden;">
        <!-- Header Section -->
        <div style="background: #d8d8d8; color: #000000; padding: 20px; text-align: left; display: flex; justify-content: space-between!important; align-items: center;">
          <!-- Company Logo on the Left -->
          <div style="flex-shrink: 0;width: 200px;">
            <img src="https://rachana-power.frappe.cloud/files/logo.png" alt="Company Logo" style="width: 200px;" />
          </div>
          <!-- Order Details on the Right -->
          <div style="text-align: right;width:600px;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;">Purchase Order</h1>
            <p style="margin: 5px 0 0; font-size: 14px;"><b>Order ID:</b> {doc.name} <br> <b>Date:</b> {doc.get_formatted("transaction_date")}</p>
          </div>
        </div>

        <!-- Vendor and Shipping Details Section -->
        <div style="padding: 20px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
          <!-- Vendor Details -->
          <div style="width: 48%; background: #f9f9f9; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="margin-top: 0; color: #000; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 5px;">Vendor Details</h3>
            <p style="margin: 10px 0; font-size: 14px;"><strong>Supplier:</strong> {doc.supplier}</p>
            <p style="margin: 10px 0; font-size: 14px;"><strong>Contact Person:</strong> {doc.contact_display or ""}</p>
            <p style="margin: 10px 0; font-size: 14px;"><strong>Email:</strong> {doc.contact_email or ""}</p>
            <p style="margin: 10px 0; font-size: 14px;"><strong>Phone:</strong> {doc.contact_mobile or ""}</p>
          </div>

          <!-- Shipping Details -->
          <div style="width: 48%; background: #f9f9f9; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h3 style="margin-top: 0; color: #000; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 5px;">Shipping Details</h3>
            <p style="margin: 10px 0; font-size: 14px;display:inline-flex;">
                <strong>Address:</strong> <span>{address}</span>
            </p>
            <p style="margin: 10px 0; font-size: 14px;">
                <strong>Required Date:</strong> {doc.get_formatted("schedule_date")}
            </p>
          </div>
        </div>

        <!-- Items Table -->
        <div style="padding: 20px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 10px;">
            <thead>
              <tr style="background-color: #d8d8d8; color: #000;">
                <th style="padding: 10px; border: 1px solid #000;text-align:center;">No.</th>
                <th style="padding: 10px; border: 1px solid #000;">Item</th>
                <th style="border: 1px solid #111; width: 85px; text-align: center;">HSN/SAC</th>
                <th style="padding: 10px; border: 1px solid #000; text-align: center;">Quantity</th>
                <th style="padding: 10px; border: 1px solid #000; text-align: center;">Rate</th>
                <th style="padding: 10px; border: 1px solid #000; text-align: center;">Amount</th>
              </tr>
            </thead>
            <tbody>
"""

    # Add table rows for items
    for index, item in enumerate(doc.items, start=1):
        row_color = "#ffffff" if index % 2 == 0 else "#f9f9f9"
        html += f"""
                <tr style="background-color: {row_color};">
                    <td style="padding: 10px; border: 1px solid #000;text-align:center;">{index}</td>
                    <td style="padding: 10px; border: 1px solid #000;">{item.description}</td>
                    <td style="border: 1px solid #111; text-align: center;">{item.gst_hsn_code}</td>
                    <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("qty")}</td>
                    <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("rate")}</td>
                    <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("amount")}</td>
                </tr>
        """

    # Add total row for items
    html += f"""
                <tr style="background-color: #f1f1f1; font-weight: bold;">
                    <td colspan="5" style="padding: 10px; text-align: right; border: 1px solid #000;">Total</td>
                    <td style="padding: 10px; border: 1px solid #000; text-align: center;">{doc.get_formatted("total")}</td>
                </tr>
                </tbody>
            </table>
            </div>

        """
    if doc.taxes:
        html += f"""
             <div class="taxes" style="padding: 20px;">
                <table style="border: 1px solid #111; width: 100%; font-family: 'Helvetica Neue', Arial, sans-serif; border-collapse: collapse; font-size: 13px;" class="tax_tab">
    <thead style="background-color: #cbcbcb;">
        <tr>
            <th rowspan="2" style="border: 1px solid #111; width: 85px; text-align: center;">HSN/SAC</th>
            <th rowspan="2" style="border: 1px solid #111;">Taxable Value</th>
            <th colspan="2" style="border: 1px solid #111;">CGST</th>
            <th colspan="2" style="border: 1px solid #111;">SGST/UTGST</th>
            <th rowspan="2" style="border: 1px solid #111; text-align: center;">Total Tax Amount</th>
        </tr>
      <tr>
                
            <th style="border: 1px solid #111;">Rate</th>
            <th style="border: 1px solid #111;">Amount</th>
            <th style="border: 1px solid #111;">Rate</th>
            <th style="border: 1px solid #111;">Amount</th>
        </tr>
    </thead>
    <tbody>
        """

        # Add tax data for items
        for item in doc.items:
            html += f"""
            <tr>
                <td style="border: 1px solid #111; padding: 8px; text-align: center;">{item.gst_hsn_code}</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{item.get_formatted("net_amount")}</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{item.cgst_rate}%</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{item.get_formatted("cgst_amount")}</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{item.sgst_rate}%</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{item.get_formatted("sgst_amount")}</td>
                <td style="border: 1px solid #111; padding: 8px; text-align: right;">{frappe.format(item.cgst_amount + item.sgst_amount, {"fieldtype": "Currency", "options": doc.currency})}</td>
                
            </tr>
            """
    # Ensure 'items' is a list; if missing or invalid, default to an empty list
        items = doc.get('items') or []
        if not isinstance(items, list):
            items = []

        # Initialize totals
        cgst_total = 0
        sgst_total = 0

        # Safely iterate through items and calculate totals
        for item in items:
            cgst_total += flt(item.get('cgst_amount', 0))
            sgst_total += flt(item.get('sgst_amount', 0))

        # Combine the totals
        total_tax = cgst_total + sgst_total

        # Format the combined total using the document's currency
        total_tax_val = frappe.format(total_tax, {"fieldtype": "Currency", "options": doc.get('currency')})
        
        
        # total_tax = cgst_total + sgst_total
        html += f"""
                <tr style="background-color: #f1f1f1; font-weight: bold;">
                        <td colspan="6" style="padding: 10px; text-align: right; border: 1px solid #000;">Total</td>
                        <td style="padding: 10px; border: 1px solid #000; text-align: center;">{total_tax_val}</td>
                    </tr>
                </tbody>
            </table>
            </div>

    """
    if doc.tc_name:
        html += f"""
        <div style="padding: 20px;">
            <div style="margin-top: 20px; background: #f9f9f9; border-left: 4px solid #0056b3; border-radius: 5px; padding: 10px;">
                <h3 style="margin-top: 0; color: #0056b3; font-size: 16px;">Terms and Conditions</h3>
                <p style="font-size: 14px;">{doc.terms}</p>
            </div>
        </div>
        """

    html += """        
      </div>
    </body>
    </html>"""
   

    if supplier_email:
      # Send the email asynchronously using frappe.enqueue
      frappe.enqueue(
          send_email_in_background,
          recipients=supplier_email.email_id,
          subject=f"Purchase Order - {doc.name}",
          message=html,
      )

def send_email_in_background(recipients, subject, message):
    """Helper function to send the email in background."""
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message,
    )
    frappe.email.queue.flush()






# import frappe

# def send_purchase_order_email(doc, method):
#     # Fetching shipping address details if available
#     ship_addr = {}
#     if doc.shipping_address:
#         ship_addr = frappe.db.get_value(
#             "Address",
#             doc.shipping_address,
#             ["address_line1", "address_line2", "city", "state", "pincode"],
#             as_dict=True
#         ) or {}

#     # Assuming ship_addr is a dictionary-like object
#     address_parts = []

#     # Add address line 1 if available
#     if ship_addr.get("address_line1"):
#         address_parts.append(ship_addr["address_line1"])

#     # Add address line 2 if available
#     if ship_addr.get("address_line2"):
#         address_parts.append(ship_addr["address_line2"])

#     # Add city if available
#     if ship_addr.get("city"):
#         address_parts.append(ship_addr["city"])

#     # Add state if available
#     if ship_addr.get("state"):
#         address_parts.append(ship_addr["state"])

#     # Add pincode if available
#     if ship_addr.get("pincode"):
#         address_parts.append(ship_addr["pincode"])

#     # Join all parts with commas and a space
#     address = ", ".join(address_parts)

#     # Constructing the HTML with inline styles
#     html = f"""
#     <html lang="en">
#     <head>
#       <meta charset="UTF-8">
#       <meta name="viewport" content="width=device-width, initial-scale=1.0">
#       <title>Purchase Order</title>
#     </head>
#     <body style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; line-height: 1.6;">
#       <div style="max-width: 700px; margin: 30px auto; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); overflow: hidden;">
#         <!-- Header Section -->
#         <div style="background: #0056b3; color: #000; padding: 20px; text-align: center;">
#           <h1 style="margin: 0; font-size: 22px; font-weight: bold;">Purchase Order</h1>
#           <p style="margin: 5px 0 0; font-size: 14px;">Order ID: {doc.name} | Date: {doc.get_formatted("transaction_date")}</p>
#         </div>

#         <!-- Vendor and Shipping Details Section -->
#         <div style="padding: 20px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
#           <!-- Vendor Details -->
#           <div style="width: 48%; background: #f9f9f9; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
#             <h3 style="margin-top: 0; color: #0056b3; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 5px;">Vendor Details</h3>
#             <p style="margin: 10px 0; font-size: 14px;"><strong>Supplier:</strong> {doc.supplier}</p>
#             <p style="margin: 10px 0; font-size: 14px;"><strong>Contact Person:</strong> {doc.contact_display or ""}</p>
#             <p style="margin: 10px 0; font-size: 14px;"><strong>Email:</strong> {doc.contact_email or ""}</p>
#             <p style="margin: 10px 0; font-size: 14px;"><strong>Phone:</strong> {doc.contact_mobile or ""}</p>
#           </div>

#           <!-- Shipping Details -->
#           <div style="width: 48%; background: #f9f9f9; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
#             <h3 style="margin-top: 0; color: #0056b3; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 5px;">Shipping Details</h3>
#             <p style="margin: 10px 0; font-size: 14px;display:inline-flex;">
#                 <strong>Address:</strong> <span>{address}</span>
#             </p>
#             <p style="margin: 10px 0; font-size: 14px;">
#                 <strong>Required Date:</strong> {doc.get_formatted("schedule_date")}
#             </p>
#           </div>
#         </div>

#         <!-- Items Table -->
#         <div style="padding: 20px;">
#           <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 10px;">
#             <thead>
#               <tr style="background-color: #0056b3; color: #000;">
#                 <th style="padding: 10px; border: 1px solid #000;">#</th>
#                 <th style="padding: 10px; border: 1px solid #000;">Item</th>
#                 <th style="padding: 10px; border: 1px solid #000; text-align: center;">Quantity</th>
#                 <th style="padding: 10px; border: 1px solid #000; text-align: center;">Rate</th>
#                 <th style="padding: 10px; border: 1px solid #000; text-align: center;">Amount</th>
#               </tr>
#             </thead>
#             <tbody>
#     """

#     # Add table rows for items
#     for index, item in enumerate(doc.items, start=1):
#         row_color = "#ffffff" if index % 2 == 0 else "#f9f9f9"
#         html += f"""
#               <tr style="background-color: {row_color};">
#                 <td style="padding: 10px; border: 1px solid #000;">{index}</td>
#                 <td style="padding: 10px; border: 1px solid #000;">{item.description}</td>
#                 <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("qty")}</td>
#                 <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("rate")}</td>
#                 <td style="padding: 10px; border: 1px solid #000; text-align: center;">{item.get_formatted("amount")}</td>
#               </tr>
#         """

#     # Add total row
#     html += f"""
#               <tr style="background-color: #f1f1f1; font-weight: bold;">
#                 <td colspan="4" style="padding: 10px; text-align: right; border: 1px solid #000;">Total</td>
#                 <td style="padding: 10px; border: 1px solid #000; text-align: center;">{doc.get_formatted("total")}</td>
#               </tr>
#             </tbody>
#           </table>
#         </div>

#     """

#     if doc.tc_name:
#         html += f"""
#         <div style="padding: 20px;">
#             <div style="margin-top: 20px; background: #f9f9f9; border-left: 4px solid #0056b3; border-radius: 5px; padding: 10px;">
#                 <h3 style="margin-top: 0; color: #0056b3; font-size: 16px;">Terms and Conditions</h3>
#                 <p style="font-size: 14px;">{doc.terms}</p>
#             </div>
#         </div>
#         """

#     html += """        
#       </div>
#     </body>
#     </html>
#     """

#     # Send the email asynchronously using frappe.enqueue
#     frappe.enqueue(
#         send_email_in_background,
#         recipients="darshpatelvadadoriya@gmail.com",
#         subject=f"Purchase Order - {doc.name}",
#         message=html,
#     )

# def send_email_in_background(recipients, subject, message):
#     """Helper function to send the email in background."""
#     frappe.sendmail(
#         recipients=recipients,
#         subject=subject,
#         message=message,
#     )
#     frappe.email.queue.flush()



