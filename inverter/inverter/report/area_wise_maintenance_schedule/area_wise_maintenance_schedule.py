# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate

def execute(filters=None):
    filters = filters or {}

  
    columns, data = [], []

    # Define static columns
    columns = [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Maintenance Schedule", "fieldname": "schedule_name", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 200},
        {"label": "Product", "fieldname": "product", "fieldtype": "Data", "width": 150},
        {"label": "Locality", "fieldname": "locality", "fieldtype": "Link", "options": "Locality", "width": 150},
    ]

    # Initialize conditions
    conditions = {}
    if filters.get("customer"):
        conditions["customer"] = filters["customer"]
    if filters.get("locality"):
        conditions["custom_locality"] = filters["locality"]

    # Handle financial year filter
    try:
        if filters.get("financial_year"):
            start_date, end_date = get_financial_year_dates(filters["financial_year"])
            conditions["scheduled_date"] = ["between", [start_date, end_date]]
    except Exception as e:
        frappe.throw(f"Error in financial year filter: {str(e)}")

    # Fetch Maintenance Schedules
    try:
        schedules = frappe.get_all(
            "Maintenance Schedule",
            fields=["name", "customer", "custom_locality"],
            filters=conditions,
        )
    except Exception as e:
        frappe.throw(f"Error fetching maintenance schedules: {str(e)}")

    # Fetch Maintenance Schedule Details
    try:
        schedule_details = frappe.get_all(
            "Maintenance Schedule Detail",
            fields=["item_code", "parent", "scheduled_date"],
            # filters=conditions,
            order_by="scheduled_date asc",
        )
    except Exception as e:
        frappe.throw(f"Error fetching schedule details: {str(e)}")

    # Map details to schedules
    max_visits = 0
    schedule_map = {}
    product_map = {}
    for detail in schedule_details:
        parent = detail.get("parent")
        if not parent:
            continue
        if parent not in schedule_map:
            schedule_map[parent] = []
            product_map[parent] = detail.get("item_code", "")
        schedule_map[parent].append(detail["scheduled_date"])
        max_visits = max(max_visits, len(schedule_map[parent]))

    # Add dynamic columns for visits
    for i in range(1, max_visits + 1):
        columns.append(
            {"label": f"{i} Visit", "fieldname": f"visit_{i}", "fieldtype": "Date", "width": 150}
        )

    # Populate data
    for schedule in schedules:
        row = {
            "customer": schedule["customer"],
            "schedule_name": schedule["name"],
            "product": product_map.get(schedule["name"], ""),
            "locality": schedule["custom_locality"],
        }
        visits = schedule_map.get(schedule["name"], [])
        for idx, visit_date in enumerate(visits):
            row[f"visit_{idx + 1}"] = visit_date

        data.append(row)

    return columns, data


def get_financial_year_dates(financial_year):
    """Returns the start and end dates of a financial year."""
    try:
        start_year, end_year = map(int, financial_year.split("-"))
        start_date = f"{start_year}-04-01"
        end_date = f"{end_year}-03-31"
        return start_date, end_date
    except ValueError:
        frappe.throw("Invalid financial year format. Expected format: YYYY-YYYY")

