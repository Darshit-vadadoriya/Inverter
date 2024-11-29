# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):
    """
    Main function for the script report. Fetches columns and data.
    """
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """
    Returns the columns to be displayed in the report.
    """
    return [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "Maintenance Schedule ID", "fieldname": "maintenance_schedule", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 220},
        {"label": "Product", "fieldname": "item_code", "width": 200},
        {"label": "Locality", "fieldname": "custom_locality", "fieldtype": "Data", "width": 180},
        {"label": "Scheduled Date", "fieldname": "scheduled_date", "fieldtype": "Date", "width": 140},
        {"label": "Delay (In Days)", "fieldname": "days_difference", "fieldtype": "Int", "width": 120},
    ]


def get_data(filters):
    """
    Fetches the data for the report based on the filters provided.
    """

    # Build query with conditions
    conditions = get_conditions(filters)
    query = f"""
        SELECT
            ms.customer,
            ms.name AS maintenance_schedule,
            ms.custom_locality,
            msd.item_code,
            msd.scheduled_date,
            msd.completion_status,
            CASE
                WHEN msd.scheduled_date < CURDATE() THEN DATEDIFF(CURDATE(), msd.scheduled_date)
                ELSE 0
            END AS days_difference
        FROM
            `tabMaintenance Schedule Detail` msd
        LEFT JOIN
            `tabMaintenance Schedule` ms ON msd.parent = ms.name
        WHERE
            ms.docstatus = 1
            AND msd.completion_status = "Pending"
            {conditions}
        ORDER BY
            msd.scheduled_date ASC
    """

    # Log the final query for debugging
    
    # Execute the query and fetch data
    try:
        result = frappe.db.sql(query, filters, as_dict=True)

        # Process results
        for row in result:
            # Here, we ensure the result is correctly processed
            pass

        return result

    except Exception as e:
        return []

def get_conditions(filters):
    """
    Builds the WHERE clause for the SQL query based on the provided filters.
    """
    conditions = []
    
    if filters.get("customer"):
        conditions.append("ms.customer = %(customer)s")
    
    if filters.get("from_date"):
        conditions.append("msd.scheduled_date >= %(from_date)s")
    
    if filters.get("to_date"):
        conditions.append("msd.scheduled_date <= %(to_date)s")
    
    if filters.get("custom_locality"):
        print(filters.get("custom_locality"))
        print("\n\n\n\n\n\n\n")
        conditions.append("ms.custom_locality = %(custom_locality)s")
    
    if filters.get("company"):
        conditions.append("ms.company = %(company)s")
    
    if filters.get("financial_year"):
        # Extract the financial year and validate the format
        financial_year = filters["financial_year"]
        if len(financial_year.split("-")) == 2:
            fy_start, fy_end = financial_year.split("-")
            try:
                fy_start = int(fy_start)
                fy_end = int(fy_end)
                fy_start_date = f"{fy_start}-04-01"
                fy_end_date = f"{fy_end}-03-31"
                conditions.append("msd.scheduled_date BETWEEN %(fy_start_date)s AND %(fy_end_date)s")
                filters["fy_start_date"] = fy_start_date
                filters["fy_end_date"] = fy_end_date
            except ValueError:
                raise ValueError("Invalid financial year")
        else:
            raise ValueError("Invalid financial year format. Expected format: YYYY-YYYY")
    
    # Combine conditions with AND
    return " AND " + " AND ".join(conditions) if conditions else ""



def get_financial_year_range(financial_year):
    """Returns the start and end dates of a financial year."""
    try:
        start_year, end_year = map(int, financial_year.split("-"))
        start_date = f"{start_year}-04-01"
        end_date = f"{end_year}-03-31"
        return start_date, end_date
    except ValueError:
        frappe.throw("Invalid financial year format. Expected format: YYYY-YYYY")
