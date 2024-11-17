# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
def execute(filters=None):
    columns = [
        {"label": "Maintenance ID", "fieldname": "name", "fieldtype": "Link", "options": "Maintenance Schedule"},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Scheduled Date", "fieldname": "scheduled_date", "fieldtype": "Date"},
        {"label": "Technician", "fieldname": "technician", "fieldtype": "Link", "options": "Employee"},
        {"label": "Actual Visit Date", "fieldname": "actual_visit_date", "fieldtype": "Date"},
        {"label": "Completion Status", "fieldname": "completion_status", "fieldtype": "Data"}
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
            msd.completion_status
        FROM 
            `tabMaintenance Schedule Detail` msd
        INNER JOIN 
            `tabMaintenance Schedule` ms ON ms.name = msd.parent
        WHERE 
            1 = 1
    """
    
    conditions = []
    values = []

    if filters.get("technician"):
        conditions.append("msd.custom_technician = %s")
        values.append(filters["technician"])
    
    if filters.get("from_scheduled_date") and filters.get("to_scheduled_date"):
        conditions.append("msd.scheduled_date BETWEEN %s AND %s")
        values.append(filters["from_scheduled_date"])
        values.append(filters["to_scheduled_date"])

    if conditions:
        query += " AND " + " AND ".join(conditions)

    maintenance_details = frappe.db.sql(query, values, as_dict=True)

    for detail in maintenance_details:
        data.append({
            "name": detail.name,
            "customer": detail.customer,
            "item_code": detail.item_code,
            "scheduled_date": detail.scheduled_date,
            "technician": detail.technician,
            "actual_visit_date": detail.actual_visit_date,
            "completion_status": detail.completion_status
        })

    return columns, data

