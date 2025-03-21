// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Technician Wise Assign and Completed Visit"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_default("company"),
        },
        {
            "label": __("Locality"),
            "fieldname": "locality",
            "fieldtype": "Link",
            "options": "Locality",
        },
        {
            "label": __("Technician"),
            "fieldname": "technician",
            "fieldtype": "Link",
            "options": "Employee",
            "get_query": function() {
                if (frappe.user_roles.includes("Technician") && !frappe.user_roles.includes("Admin")) {
                    return {
                        filters: {
                            user_id: frappe.session.user // Filter by the current session's user
                        }
                    };
                }
            },
        },
        {
            "label": __("From Scheduled Date"),
            "fieldname": "from_scheduled_date",
            "fieldtype": "Date",
            "default": get_date_30_days_ago()
        },
        {
            "label": __("To Scheduled Date"),
            "fieldname": "to_scheduled_date",
            "fieldtype": "Date",
            "default": get_today_date()
        },
    ],
    onload: function (report) {
        // Fetch the Employee linked to the current session user
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Employee",
                fieldname: "name",
                filters: {
                    user_id: frappe.session.user
                }
            },
            callback: function (response) {
                if (response.message) {
                    // Set the "technician" filter value to the fetched Employee name
                    frappe.query_report.set_filter_value("technician", response.message.name);
                }
            }
        });

        
    },
};

// Helper function to get the date 30 days ago
function get_date_30_days_ago() {
    var date = new Date();
    date.setDate(date.getDate() - 30); // Subtract 30 days from today
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}

// Helper function to get today's date
function get_today_date() {
    var date = new Date();
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}


