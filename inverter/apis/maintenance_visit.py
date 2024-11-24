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



