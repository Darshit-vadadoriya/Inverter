# Copyright (c) 2024, Sahil Patel and contributors
# For license information, please see license.txt
import frappe
from datetime import datetime

# def execute(filters=None):
#     filters = set_default_financial_year(filters)
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Locality", "fieldname": "locality", "fieldtype": "Data", "width": 150},
#         {"label": "April", "fieldname": "april", "fieldtype": "Int", "width": 100},
#         {"label": "May", "fieldname": "may", "fieldtype": "Int", "width": 100},
#         {"label": "June", "fieldname": "june", "fieldtype": "Int", "width": 100},
#         {"label": "July", "fieldname": "july", "fieldtype": "Int", "width": 100},
#         {"label": "August", "fieldname": "august", "fieldtype": "Int", "width": 100},
#         {"label": "September", "fieldname": "september", "fieldtype": "Int", "width": 100},
#         {"label": "October", "fieldname": "october", "fieldtype": "Int", "width": 100},
#         {"label": "November", "fieldname": "november", "fieldtype": "Int", "width": 100},
#         {"label": "December", "fieldname": "december", "fieldtype": "Int", "width": 100},
#         {"label": "January", "fieldname": "january", "fieldtype": "Int", "width": 100},
#         {"label": "February", "fieldname": "february", "fieldtype": "Int", "width": 100},
#         {"label": "March", "fieldname": "march", "fieldtype": "Int", "width": 100},
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
#     query = """
# SELECT 
#     IFNULL(YEAR(msd.actual_date), YEAR(CURDATE())) AS year,
#     lm.locality_name AS locality,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 1 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS january,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 2 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS february,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 3 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS march,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 4 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS april,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 5 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS may,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 6 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS june,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 7 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS july,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 8 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS august,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 9 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS september,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 10 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS october,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 11 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS november,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 12 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS december
# FROM 
#     `tabLocality` lm
# LEFT JOIN 
#     `tabMaintenance Schedule` ms ON lm.name = ms.custom_locality
# LEFT JOIN 
#     `tabMaintenance Schedule Detail` msd 
#     ON msd.parent = ms.name 
#     AND msd.actual_date IS NOT NULL
# WHERE 1=1 {conditions} 
# GROUP BY 
#     lm.locality_name, year
# ORDER BY 
#     year, lm.locality_name
# """.format(conditions=conditions)
#     return frappe.db.sql(query, as_dict=True)



# def get_conditions(filters):
#     conditions = ""
#     if filters.get("financial_year"):
#         financial_year = filters.get("financial_year")
#         start_date, end_date = get_financial_year_dates(financial_year)
#         conditions += " AND msd.actual_date BETWEEN '{}' AND '{}'".format(start_date, end_date)
#     if filters.get("company"):
#         company = filters.get("company")
#         conditions += " AND ms.company = '{}'".format(company)
#     return conditions
	

# def get_financial_year_dates(financial_year):
#     """
#     Returns the start and end dates for a financial year.
#     Assumes financial year starts in April and ends in March.
#     """
#     start_year = int(financial_year.split("-")[0])
#     end_year = start_year + 1
#     start_date = "{}-04-01".format(start_year)
#     end_date = "{}-03-31".format(end_year)
#     return start_date, end_date

# def set_default_financial_year(filters):
#     """
#     Sets the current financial year as the default if no financial year is provided.
#     """
#     if not filters:
#         filters = {}

#     if not filters.get("financial_year"):
#         current_date = datetime.now()
#         if current_date.month >= 4:
#             start_year = current_date.year
#             end_year = current_date.year + 1
#         else:
#             start_year = current_date.year - 1
#             end_year = current_date.year
#         filters["financial_year"] = "{}-{}".format(start_year, end_year)
    
#     return filters


# ====================================== REPORT

# def execute(filters=None):
#     filters = set_default_financial_year(filters)
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Locality", "fieldname": "locality", "fieldtype": "Data", "width": 150},
#         {"label": "April", "fieldname": "april", "fieldtype": "Int", "width": 100},
#         {"label": "May", "fieldname": "may", "fieldtype": "Int", "width": 100},
#         {"label": "June", "fieldname": "june", "fieldtype": "Int", "width": 100},
#         {"label": "July", "fieldname": "july", "fieldtype": "Int", "width": 100},
#         {"label": "August", "fieldname": "august", "fieldtype": "Int", "width": 100},
#         {"label": "September", "fieldname": "september", "fieldtype": "Int", "width": 100},
#         {"label": "October", "fieldname": "october", "fieldtype": "Int", "width": 100},
#         {"label": "November", "fieldname": "november", "fieldtype": "Int", "width": 100},
#         {"label": "December", "fieldname": "december", "fieldtype": "Int", "width": 100},
#         {"label": "January", "fieldname": "january", "fieldtype": "Int", "width": 100},
#         {"label": "February", "fieldname": "february", "fieldtype": "Int", "width": 100},
#         {"label": "March", "fieldname": "march", "fieldtype": "Int", "width": 100},
#     ]

# def get_data(filters):
#     conditions = get_conditions(filters)
#     query = """
# SELECT 
#     IFNULL(YEAR(msd.actual_date), YEAR(CURDATE())) AS year,
#     lm.locality_name AS locality,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 1 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS january,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 2 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS february,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 3 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS march,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 4 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS april,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 5 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS may,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 6 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS june,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 7 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS july,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 8 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS august,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 9 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS september,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 10 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS october,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 11 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS november,
#     SUM(CASE WHEN MONTH(msd.actual_date) = 12 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS december
# FROM 
#     `tabLocality` lm
# LEFT JOIN 
#     `tabMaintenance Schedule` ms ON lm.name = ms.custom_locality
# LEFT JOIN 
#     `tabMaintenance Schedule Detail` msd 
#     ON msd.parent = ms.name 
#     AND msd.actual_date IS NOT NULL
# LEFT JOIN 
#     `tabItem` item ON msd.item_code = item.item_code
# WHERE 1=1 {conditions} 
# GROUP BY 
#     lm.locality_name, year
# ORDER BY 
#     year, lm.locality_name
# """.format(conditions=conditions)
#     return frappe.db.sql(query, as_dict=True)

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("financial_year"):
#         financial_year = filters.get("financial_year")
#         start_date, end_date = get_financial_year_dates(financial_year)
#         conditions += " AND msd.actual_date BETWEEN '{}' AND '{}'".format(start_date, end_date)
#     if filters.get("company"):
#         company = filters.get("company")
#         conditions += " AND ms.company = '{}'".format(company)
#     if filters.get("product_group"):
#         product_group = filters.get("product_group")
#         conditions += " AND item.custom_product_group = '{}'".format(product_group)
#     return conditions

# def get_financial_year_dates(financial_year):
#     """
#     Returns the start and end dates for a financial year.
#     Assumes financial year starts in April and ends in March.
#     """
#     start_year = int(financial_year.split("-")[0])
#     end_year = start_year + 1
#     start_date = "{}-04-01".format(start_year)
#     end_date = "{}-03-31".format(end_year)
#     return start_date, end_date

# def set_default_financial_year(filters):
#     """
#     Sets the current financial year as the default if no financial year is provided.
#     """
#     if not filters:
#         filters = {}

#     if not filters.get("financial_year"):
#         current_date = datetime.now()
#         if current_date.month >= 4:
#             start_year = current_date.year
#             end_year = current_date.year + 1
#         else:
#             start_year = current_date.year - 1
#             end_year = current_date.year
#         filters["financial_year"] = "{}-{}".format(start_year, end_year)
    
#     return filters







import frappe
from datetime import datetime

def execute(filters=None):
    # Set default financial year if not provided
    filters = set_default_financial_year(filters)
    
    # Get the columns for the report
    columns = get_columns()
    
    # Fetch data based on the filters
    data = get_data(filters)
    
    return columns, data

def get_columns():
    """
    This function defines the columns for the report.
    """
    return [
        {"label": "Locality", "fieldname": "locality", "fieldtype": "Data", "width": 150},
        {"label": "April", "fieldname": "april", "fieldtype": "Int", "width": 100},
        {"label": "May", "fieldname": "may", "fieldtype": "Int", "width": 100},
        {"label": "June", "fieldname": "june", "fieldtype": "Int", "width": 100},
        {"label": "July", "fieldname": "july", "fieldtype": "Int", "width": 100},
        {"label": "August", "fieldname": "august", "fieldtype": "Int", "width": 100},
        {"label": "September", "fieldname": "september", "fieldtype": "Int", "width": 100},
        {"label": "October", "fieldname": "october", "fieldtype": "Int", "width": 100},
        {"label": "November", "fieldname": "november", "fieldtype": "Int", "width": 100},
        {"label": "December", "fieldname": "december", "fieldtype": "Int", "width": 100},
        {"label": "January", "fieldname": "january", "fieldtype": "Int", "width": 100},
        {"label": "February", "fieldname": "february", "fieldtype": "Int", "width": 100},
        {"label": "March", "fieldname": "march", "fieldtype": "Int", "width": 100},
    ]
def get_data(filters):
    """
    Fetches the data based on the provided filters while ensuring all localities are shown,
    and only submitted maintenance schedules are considered.
    """
    # Generate conditions for date, company, and product group
    conditions, product_condition = get_conditions(filters)
    
    # Base query with placeholders for dynamic conditions
    query = f"""
        SELECT 
            lm.locality_name AS locality,
            SUM(CASE WHEN MONTH(msd.actual_date) = 1 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS january,
            SUM(CASE WHEN MONTH(msd.actual_date) = 2 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS february,
            SUM(CASE WHEN MONTH(msd.actual_date) = 3 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS march,
            SUM(CASE WHEN MONTH(msd.actual_date) = 4 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS april,
            SUM(CASE WHEN MONTH(msd.actual_date) = 5 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS may,
            SUM(CASE WHEN MONTH(msd.actual_date) = 6 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS june,
            SUM(CASE WHEN MONTH(msd.actual_date) = 7 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS july,
            SUM(CASE WHEN MONTH(msd.actual_date) = 8 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS august,
            SUM(CASE WHEN MONTH(msd.actual_date) = 9 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS september,
            SUM(CASE WHEN MONTH(msd.actual_date) = 10 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS october,
            SUM(CASE WHEN MONTH(msd.actual_date) = 11 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS november,
            SUM(CASE WHEN MONTH(msd.actual_date) = 12 AND msd.completion_status = 'Fully Completed' THEN 1 ELSE 0 END) AS december
        FROM 
            `tabLocality` lm
        LEFT JOIN 
            `tabMaintenance Schedule` ms 
            ON lm.name = ms.custom_locality 
            AND ms.docstatus = 1  -- Only include submitted maintenance schedules
        LEFT JOIN 
            `tabMaintenance Schedule Detail` msd 
            ON msd.parent = ms.name 
        LEFT JOIN 
            `tabItem` item 
            ON msd.item_code = item.item_code  
        WHERE 
            1=1  
            AND (lm.name = ms.custom_locality OR ms.custom_locality != lm.name)
            {product_condition}
            {conditions}
        GROUP BY 
            lm.locality_name
        ORDER BY 
            lm.locality_name;
    """
    
    print(query)  # Debug: Print query to verify correctness
    # Execute and return query results
    return frappe.db.sql(query, as_dict=True)

def get_conditions(filters):
    """
    Adds conditions based on the provided filters without excluding rows from Locality.
    """
    conditions = ""
    product_condition = ""
    
    # Financial Year Filter
    if filters.get("financial_year"):
        financial_year = filters["financial_year"]
        start_date, end_date = get_financial_year_dates(financial_year)
        conditions += f" AND msd.actual_date BETWEEN '{start_date}' AND '{end_date}'"
    
    # Company Filter
    if filters.get("company"):
        company = filters["company"]
        conditions += f" AND ms.company = '{company}'"
    
    # Product Group Filter
    if filters.get("product_group"):
        product_group = filters["product_group"]
        product_condition += f" AND item.custom_product_group = '{product_group}'"
    
    return conditions, product_condition
   

def get_financial_year_dates(financial_year):
    """
    Returns the start and end dates for the given financial year.
    Assumes the financial year starts in April and ends in March.
    """
    start_year = int(financial_year.split("-")[0])
    end_year = start_year + 1
    start_date = "{}-04-01".format(start_year)
    end_date = "{}-03-31".format(end_year)
    return start_date, end_date

def set_default_financial_year(filters):
    """
    Sets the current financial year as the default if not provided.
    """
    if not filters:
        filters = {}
    
    if not filters.get("financial_year"):
        current_date = datetime.now()
        if current_date.month >= 4:
            start_year = current_date.year
            end_year = current_date.year + 1
        else:
            start_year = current_date.year - 1
            end_year = current_date.year
        filters["financial_year"] = "{}-{}".format(start_year, end_year)
    
    return filters





