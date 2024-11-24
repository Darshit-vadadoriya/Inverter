# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe


from datetime import date

def execute(filters=None):
    columns = [
        {"label": "Maintenance ID", "fieldname": "name", "fieldtype": "Link", "options": "Maintenance Schedule","width": 200},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer","width": 150},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Scheduled Date", "fieldname": "scheduled_date", "fieldtype": "Date"},
        {"label": "Technician", "fieldname": "technician", "fieldtype": "Link", "options": "Employee"},
        {"label": "Actual Visit Date", "fieldname": "actual_visit_date", "fieldtype": "Date"},
        {"label": "Completion Status", "fieldname": "completion_status", "fieldtype": "Data"},
        {"label": "Area", "fieldname": "area", "fieldtype": "Data","width": 200},
        {"label": "Delayed (in days)", "fieldname": "delayed_days", "fieldtype": "Int", "width": 150}
    ]

    data = []

    query = """
        SELECT 
            msd.parent AS name,
            ms.customer,
            msd.item_code,
            msd.scheduled_date,
            msd.custom_technician AS technician,
            msd.actual_date AS actual_visit_date,
            msd.completion_status,
            ms.custom_locality AS area
        FROM 
            `tabMaintenance Schedule Detail` msd
        INNER JOIN 
            `tabMaintenance Schedule` ms ON ms.name = msd.parent
        WHERE 
            1 = 1
    """
    
    conditions = []
    values = []

    # Filter by technician if provided
    if filters.get("technician"):
        conditions.append("msd.custom_technician = %s")
        values.append(filters["technician"])
    
    # Filter by scheduled date range if provided
    if filters.get("from_scheduled_date") and filters.get("to_scheduled_date"):
        conditions.append("msd.scheduled_date BETWEEN %s AND %s")
        values.append(filters["from_scheduled_date"])
        values.append(filters["to_scheduled_date"])
    
    # Filter by locality if provided
    if filters.get("locality"):
        conditions.append("ms.custom_locality = %s")
        values.append(filters["locality"])

    # Add conditions to the query if any
    if conditions:
        query += " AND " + " AND ".join(conditions)

    # Execute the query
    maintenance_details = frappe.db.sql(query, values, as_dict=True)

    # Prepare the data for the report
    today = date.today()

    for detail in maintenance_details:
        scheduled_date = detail.scheduled_date
        actual_visit_date = detail.actual_visit_date
        delayed_days = None

        # Calculate delayed days
        if scheduled_date:
            if actual_visit_date:
                delayed_days = (actual_visit_date - scheduled_date).days
            else:
                if today < scheduled_date:
                    delayed_days = 0  # No delay yet
                else:
                    delayed_days = (today - scheduled_date).days

        data.append({
            "name": detail.name,
            "customer": detail.customer,
            "item_code": detail.item_code,
            "scheduled_date": scheduled_date,
            "technician": detail.technician,
            "actual_visit_date": actual_visit_date,
            "completion_status": detail.completion_status,
            "area": detail.area,
            "delayed_days": delayed_days
        })

    return columns, data
    
