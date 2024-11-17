// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

// frappe.query_reports["Technician Wise Assign and Completed Visit"] = {
//     "filters": [
//         {
//             "label": __("Status"),
//             "fieldname": "status",
//             "fieldtype": "Select",
//             "options": ["","Pending", "Partially Completed", "Completed"],
//             "default": "Scheduled"
//         },
//         {
//             "label": __("Customer"),
//             "fieldname": "customer",
//             "fieldtype": "Link",
//             "options": "Customer",
//         },
//         {
//             "label": __("Scheduled Date"),
//             "fieldname": "scheduled_date",
//             "fieldtype": "DateRange",
//         },
//         {
//             "label": __("Actual Visit Date"),
//             "fieldname": "actual_date",
//             "fieldtype": "DateRange",
//         }
//     ]
// };



frappe.query_reports["Technician Wise Assign and Completed Visit"] = {
    "filters": [
      
		{
            "label": __("Technician"),
            "fieldname": "technician",
            "fieldtype": "Link",
            "options": "Technician",
        },
        {
            "label": __("From Scheduled Date"),
            "fieldname": "from_scheduled_date",
            "fieldtype": "Date",
            "default": ""
        },
		{
            "label": __("To Scheduled Date"),
            "fieldname": "to_scheduled_date",
            "fieldtype": "Date",
            "default": ""
        },
    ]
};

