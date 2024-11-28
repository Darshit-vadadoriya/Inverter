import frappe

# @frappe.whitelist()
# def get_serial_no(customer):
#     serial_numbers = frappe.db.sql("""
#             SELECT DISTINCT
#                 dni.serial_no
#             FROM
#                 `tabDelivery Note` dn
#             JOIN
#                 `tabDelivery Note Item` dni ON dni.parent = dn.name
#             WHERE
#                 dn.customer = %(customer)s
#                 AND dn.docstatus = 1
#                 AND dni.serial_no IS NOT NULL
#         """, {"customer": customer}, as_dict=True)

#     #generate filtered serial no
#     result = []
#     for row in serial_numbers:
#         if row.serial_no:
#             serial_list = row.serial_no.split("\n")  
#             cleaned_serials = [serial.strip() for serial in serial_list if serial.strip()]
#             result.extend(cleaned_serials)
#     return list(set(result))

@frappe.whitelist()
def get_serial_no(customer):
    """
    Fetch distinct serial numbers from Delivery Note Items and Serial and Batch Entry tables 
    for a given customer, and return a cleaned list of unique serial numbers.
    """
    # Fetch relevant data from Delivery Note and Serial and Batch Bundle tables
    serial_numbers = frappe.db.sql("""
        SELECT DISTINCT
            dn.name AS delivery_no,
            dni.name AS batch_bundle
        FROM
            `tabDelivery Note` dn
        JOIN
            `tabSerial and Batch Bundle` dni ON dni.voucher_no = dn.name
        WHERE
            dn.customer = %(customer)s
    """, {"customer": customer}, as_dict=True)

    if not serial_numbers:
        frappe.log_error(f"No data found for customer: {customer}", "Debug - get_serial_no")
        return []

    # Initialize a set for unique serial numbers
    result_set = set()

    # Process serial numbers from the fetched data
    for row in serial_numbers:
        delivery_no = row.get("delivery_no")
        batch_bundle = row.get("batch_bundle")

        # Fetch additional serial numbers from Serial and Batch Entry table
        if batch_bundle:
            cid_serial_numbers = frappe.db.sql("""
                SELECT DISTINCT
                    sbe.serial_no
                FROM
                    `tabSerial and Batch Entry` sbe
                JOIN
                    `tabSerial and Batch Bundle` sbb ON sbe.parent = sbb.name
                WHERE
                    sbe.parent = %(batch_bundle)s
                    AND sbb.is_cancelled = '0'
            """, {"batch_bundle": batch_bundle}, as_dict=True)

            if not cid_serial_numbers:
                frappe.log_error(f"No serial numbers found for batch_bundle: {batch_bundle}", "Debug - get_serial_no")

            for cid_row in cid_serial_numbers:
                cid_serial_no = cid_row.get("serial_no")
                if cid_serial_no:
                    cid_serial_list = [s.strip() for s in cid_serial_no.split("\n") if s.strip()]
                    result_set.update(cid_serial_list)

    # Convert set to list and return
    return list(result_set)


# get linked employee wise maintenance visit records
@frappe.whitelist()
def get_maintenance_visits_for_technician(employee):
    # Fetch Maintenance Visits where Purpose child table links to the Technician's employee
    visits = frappe.db.sql("""
        SELECT DISTINCT parent
        FROM `tabMaintenance Visit Purpose`
        WHERE custom_technician = %s
    """, (employee,), as_dict=False)

    return [visit[0] for visit in visits]



import frappe

@frappe.whitelist()
def get_technician_roles(user):
    """
    Check if the user has the 'Technician' role and fetch associated details from Maintenance Schedule Detail.
    """
    # Fetch roles of the current user
    roles = frappe.get_roles(user)

    # Check if the user has the 'Technician' role but not 'Admin' or 'System Manager'
    if "Technician" in roles and "Administrator" not in roles and "System Manager" not in roles:
        
        # Fetch the employee linked to the current user
        employee = frappe.db.get_value('Employee', {'user_id': user}, 'name')
        
        if employee:
            # If employee exists, fetch Maintenance Schedule Details for that employee
            details = frappe.db.get_all(
                'Maintenance Schedule Detail',
                filters={'custom_technician': employee},  # Assuming 'employee' field is in Maintenance Schedule Detail
                fields=["*"]
            )
            return details
        else:
            return []  # If no employee linked to user, return empty list
    else:
        # Return an empty list if the user is not a Technician or is an Admin/System Manager
        return []




@frappe.whitelist()
def get_pending_maintenance_schedules():
    # Get the current user's employee
    employee = frappe.session.user
    employee_doc = frappe.get_doc("Employee",{"user_id":employee})

    # Query for maintenance schedule details where the technician is the current user and the completion status is "Pending"
    schedules = frappe.get_all('Maintenance Schedule Detail', filters={
        'custom_technician': employee_doc.name,
        'completion_status': 'Pending'
    }, fields=['name', 'scheduled_date'])

    # Return the schedules in a format suitable for the select options
    return schedules



import frappe

@frappe.whitelist()
def get_maintenance_schedule_details(schedule_name):
    # Fetch the details of the Maintenance Schedule Detail based on schedule_name (ID)
    schedule_detail = frappe.db.get_value(
        'Maintenance Schedule Detail', 
        schedule_name, 
        ['*'],  # Fields to fetch
        as_dict=True
    )
    
    # Check if schedule detail is found
    if schedule_detail:
        # Fetch the related Maintenance Schedule (parent) document
        maintenance_schedule = frappe.db.get_value(
            'Maintenance Schedule', 
            schedule_detail.parent,  # Use the parent field to get the related schedule
            ['*'],  # Add any relevant fields
            as_dict=True
        )
        
        # Combine both schedule detail and maintenance schedule data
        combined_data = {
            'schedule_detail': schedule_detail,
            'maintenance_schedule': maintenance_schedule
        }
        
        return combined_data
    else:
        return None
