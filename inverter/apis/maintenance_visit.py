import frappe

@frappe.whitelist()
def get_serial_no(customer):
    serial_numbers = frappe.db.sql("""
            SELECT DISTINCT
                dni.serial_no
            FROM
                `tabDelivery Note` dn
            JOIN
                `tabDelivery Note Item` dni ON dni.parent = dn.name
            WHERE
                dn.customer = %(customer)s
                AND dn.docstatus = 1
                AND dni.serial_no IS NOT NULL
        """, {"customer": customer}, as_dict=True)

    #generate filtered serial no
    result = []
    for row in serial_numbers:
        if row.serial_no:
            serial_list = row.serial_no.split("\n")  
            cleaned_serials = [serial.strip() for serial in serial_list if serial.strip()]
            result.extend(cleaned_serials)
    return list(set(result))