# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt
import frappe

# from frappe.utils import today, getdate

# def execute(filters=None):
#     filters = filters or {}

#     columns, data = [], []

#     # Define static columns
#     columns = [
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
#         {"label": "Maintenance Schedule", "fieldname": "schedule_name", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 200},
#         {"label": "Product", "fieldname": "product", "fieldtype": "Data", "width": 150},
#         {"label": "Locality", "fieldname": "locality", "fieldtype": "Link", "options": "Locality", "width": 150},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 200},
#     ]

#     # Initialize conditions
#     conditions = {}
#     if filters.get("customer"):
#         conditions["customer"] = filters["customer"]
#     if filters.get("locality"):
#         conditions["custom_locality"] = filters["locality"]
#     if filters.get("company"):
#         conditions["company"] = filters["company"]

#     # Handle financial year filter
#     try:
#         if filters.get("financial_year"):
#             start_date, end_date = get_financial_year_dates(filters["financial_year"])
#             conditions["scheduled_date"] = ["between", [start_date, end_date]]
#     except Exception as e:
#         frappe.throw(f"Error in financial year filter: {str(e)}")

#     # Fetch Maintenance Schedules
#     try:
#         schedules = frappe.get_all(
#             "Maintenance Schedule",
#             fields=["name", "customer", "custom_locality", "company"],
#             filters=conditions,
#         )
#     except Exception as e:
#         frappe.throw(f"Error fetching maintenance schedules: {str(e)}")

#     # Fetch Maintenance Schedule Details
#     try:
#         schedule_details = frappe.get_all(
#             "Maintenance Schedule Detail",
#             fields=["item_code", "parent", "scheduled_date"],
#             order_by="scheduled_date asc",
#         )
#     except Exception as e:
#         frappe.throw(f"Error fetching schedule details: {str(e)}")

#     # Map details to schedules
#     max_visits = 0
#     schedule_map = {}
#     product_map = {}
#     for detail in schedule_details:
#         parent = detail.get("parent")
#         if not parent:
#             continue
#         if parent not in schedule_map:
#             schedule_map[parent] = []
#             product_map[parent] = detail.get("item_code", "")
#         schedule_map[parent].append(detail["scheduled_date"])
#         max_visits = max(max_visits, len(schedule_map[parent]))

#     # Add dynamic columns for visits
#     for i in range(1, max_visits + 1):
#         columns.append(
#             {"label": f"{i} Visit", "fieldname": f"visit_{i}", "fieldtype": "Date", "width": 150}
#         )

#     # Populate data
#     for schedule in schedules:
#         row = {
#             "customer": schedule["customer"],
#             "schedule_name": schedule["name"],
#             "product": product_map.get(schedule["name"], ""),
#             "locality": schedule["custom_locality"],
#             "company": schedule["company"],
#         }
#         visits = schedule_map.get(schedule["name"], [])
#         for idx, visit_date in enumerate(visits):
#             row[f"visit_{idx + 1}"] = visit_date

#         data.append(row)

#     return columns, data


# def get_financial_year_dates(financial_year):
#     """Returns the start and end dates of a financial year."""
#     try:
#         start_year, end_year = map(int, financial_year.split("-"))
#         start_date = f"{start_year}-04-01"
#         end_date = f"{end_year}-03-31"
#         return start_date, end_date
#     except ValueError:
#         frappe.throw("Invalid financial year format. Expected format: YYYY-YYYY")



# def execute(filters=None):
#     filters = filters or {}

#     # Define static columns
#     columns = [
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
#         {"label": "Maintenance Schedule", "fieldname": "schedule_name", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 200},
#         {"label": "Product", "fieldname": "product", "fieldtype": "Data", "width": 150},
#         {"label": "Locality", "fieldname": "locality", "fieldtype": "Link", "options": "Locality", "width": 150},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 200},
#     ]

#     # Initialize conditions for filters
#     conditions = []
#     if filters.get("customer"):
#         conditions.append(f"ms.customer = '{filters['customer']}'")
#     if filters.get("locality"):
#         conditions.append(f"ms.custom_locality = '{filters['locality']}'")
#     if filters.get("company"):
#         conditions.append(f"ms.company = '{filters['company']}'")

#     # Financial year filter
#     start_date, end_date = None, None
#     if filters.get("financial_year"):
#         try:
#             start_date, end_date = get_financial_year_dates(filters["financial_year"])
#             conditions.append(f"msd.scheduled_date BETWEEN '{start_date}' AND '{end_date}'")
#         except Exception as e:
#             frappe.throw(f"Error in financial year filter: {str(e)}")

#     # Build the WHERE clause
#     where_clause = " AND ".join(conditions) if conditions else "1=1"

#     # Fetch Maintenance Schedules with Maintenance Schedule Details using SQL JOIN
#     try:
#         query = f"""
#         SELECT 
#             ms.name AS schedule_name, 
#             ms.customer, 
#             ms.custom_locality AS locality, 
#             ms.company,
#             msd.item_code AS product,
#             msd.scheduled_date
#         FROM `tabMaintenance Schedule` ms
#         JOIN `tabMaintenance Schedule Detail` msd ON ms.name = msd.parent
#         WHERE {where_clause}
#         ORDER BY msd.scheduled_date ASC
#         """
#         schedule_details = frappe.db.sql(query, as_dict=True)
#     except Exception as e:
#         frappe.throw(f"Error fetching schedule details: {str(e)}")

#     # Process the results to determine the dynamic columns for visits
#     max_visits = 0
#     schedule_map = {}
#     product_map = {}
    
#     # Map schedule details to their schedules
#     for detail in schedule_details:
#         parent = detail.get("schedule_name")
#         if parent not in schedule_map:
#             schedule_map[parent] = []
#             product_map[parent] = detail.get("product", "")
#         if detail["scheduled_date"] not in schedule_map[parent]:
#             schedule_map[parent].append(detail["scheduled_date"])
#             max_visits = max(max_visits, len(schedule_map[parent]))

#     # Add dynamic columns for visits
#     for i in range(1, max_visits + 1):
#         columns.append(
#             {"label": f"Visit {i}", "fieldname": f"visit_{i}", "fieldtype": "Date", "width": 150}
#         )

#     # Populate data rows
#     data = []
#     for schedule in schedule_map.keys():
#         print(schedule)
#         print("\n\n\n\n\n\n\n\n\n\n\n\n\n   ")
#         # Take the first customer from the schedule details, assuming it's consistent
#         customer = schedule_details[0]["customer"]
#         row = {
#             "customer": customer,
#             "schedule_name": schedule,
#             "product": product_map.get(schedule, ""),
#             "locality": schedule_details[0]["locality"],
#             "company": schedule_details[0]["company"],
#         }
#         visits = schedule_map.get(schedule, [])
#         for idx, visit_date in enumerate(visits):
#             row[f"visit_{idx + 1}"] = visit_date
#         data.append(row)

#     return columns, data


# def get_financial_year_dates(financial_year):
#     """Returns the start and end dates of a financial year."""
#     start_year, end_year = map(int, financial_year.split("-"))
#     start_date = f"{start_year}-04-01"
#     end_date = f"{end_year}-03-31"
#     return start_date, end_date






def execute(filters=None):
    filters = filters or {}

    # Define static columns
    columns = [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Maintenance Schedule", "fieldname": "schedule_name", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 200},
        {"label": "Product", "fieldname": "product", "fieldtype": "Data", "width": 150},
        {"label": "Locality", "fieldname": "locality", "fieldtype": "Link", "options": "Locality", "width": 150},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 200},
    ]

    # Initialize conditions for filters
    conditions = []
    if filters.get("customer"):
        conditions.append(f"ms.customer = '{filters['customer']}'")
    if filters.get("locality"):
        conditions.append(f"ms.custom_locality = '{filters['locality']}'")
    if filters.get("company"):
        conditions.append(f"ms.company = '{filters['company']}'")

    # Add financial year filter
    if filters.get("financial_year"):
        try:
            start_date, end_date = get_financial_year_dates(filters["financial_year"])
            conditions.append(f"msd.scheduled_date BETWEEN '{start_date}' AND '{end_date}'")
        except Exception as e:
            frappe.throw(f"Error in financial year filter: {str(e)}")

    # Build WHERE clause
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Fetch Maintenance Schedules and Details
    query = f"""
        SELECT 
            ms.name AS schedule_name, 
            ms.customer, 
            ms.custom_locality AS locality, 
            ms.company,
            msd.item_code AS product,
            msd.scheduled_date
        FROM `tabMaintenance Schedule` ms
        JOIN `tabMaintenance Schedule Detail` msd ON ms.name = msd.parent
        WHERE {where_clause}
        ORDER BY msd.scheduled_date ASC
    """
    schedule_details = frappe.db.sql(query, as_dict=True)

    # Determine dynamic columns for visits
    max_visits = 0
    schedule_map = {}
    product_map = {}

    for detail in schedule_details:
        schedule_name = detail.get("schedule_name")
        if schedule_name not in schedule_map:
            schedule_map[schedule_name] = []
            product_map[schedule_name] = detail.get("product", "")
        if detail["scheduled_date"] not in schedule_map[schedule_name]:
            schedule_map[schedule_name].append(detail["scheduled_date"])
            max_visits = max(max_visits, len(schedule_map[schedule_name]))

    # Add dynamic columns for visits
    for i in range(1, max_visits + 1):
        columns.append(
            {"label": f"Visit {i}", "fieldname": f"visit_{i}", "fieldtype": "Date", "width": 150}
        )

    # Populate data rows
    data = []
    for schedule, visits in schedule_map.items():
        # Fetch the first matching record for static fields
        row = {
            "customer": next((d["customer"] for d in schedule_details if d["schedule_name"] == schedule), ""),
            "schedule_name": schedule,
            "product": product_map.get(schedule, ""),
            "locality": next((d["locality"] for d in schedule_details if d["schedule_name"] == schedule), ""),
            "company": next((d["company"] for d in schedule_details if d["schedule_name"] == schedule), ""),
        }
        # Add dynamic visit dates
        for idx, visit_date in enumerate(visits):
            row[f"visit_{idx + 1}"] = visit_date
        data.append(row)

    return columns, data


def get_financial_year_dates(financial_year):
    """
    Returns the start and end dates of a financial year in YYYY-MM-DD format.
    """
    start_year, end_year = map(int, financial_year.split("-"))
    start_date = f"{start_year}-04-01"
    end_date = f"{end_year}-03-31"
    return start_date, end_date
