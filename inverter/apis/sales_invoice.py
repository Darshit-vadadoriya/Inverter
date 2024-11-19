import frappe
from frappe.utils import today, add_months

def create_maintenance_schedule(doc, method):
    # frappe.db.get_value("Customer",doc.customer,"custom_locality",as_dict=True)
    for item in doc.items:
        item_details = frappe.db.get_value(
            "Item", 
            item.item_code, 
            ["custom_periodicity", "custom_no_of_visits"], 
            as_dict=True
        )
        
        
        if item_details:
            maintenance_schedule = frappe.new_doc("Maintenance Schedule")
            maintenance_schedule.customer = doc.customer
            # maintenance_schedule.custom_locality = item_details.get("custom_locality")
            maintenance_schedule.sales_invoice = doc.name
            maintenance_schedule.transaction_date = today()
            
            maintenance_schedule.append("items", {
                "item_code": item.item_code,
                "serial_no": item.serial_no,
                "qty": item.qty,
                "start_date": today(),
                "no_of_visits": item_details.get("custom_no_of_visits", 1),
                "periodicity": item_details.get("custom_periodicity", "Monthly"),
                "end_date": add_months(today(), 12)
            })
            
            maintenance_schedule.insert()
            maintenance_schedule.submit() 
    
    frappe.db.commit()
