// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

// frappe.query_reports["Technician Wise Assign and Completed Visit"] = {
//     "filters": [
//         {
//             "fieldname": "company",
//             "label": __("Company"),
//             "fieldtype": "Link",
//             "options": "Company",
//             "default": frappe.defaults.get_default("company"),
//         },
//         {
//             "label": __("Locality"),
//             "fieldname": "locality",
//             "fieldtype": "Link",
//             "options": "Locality",
//         },
// 		{
//             "label": __("Technician"),
//             "fieldname": "technician",
//             "fieldtype": "Link",
//             "options": "Employee",
//         },
//         {
//             "label": __("From Scheduled Date"),
//             "fieldname": "from_scheduled_date",
//             "fieldtype": "Date",
//             "default": get_date_30_days_ago()
//         },
// 		{
//             "label": __("To Scheduled Date"),
//             "fieldname": "to_scheduled_date",
//             "fieldtype": "Date",
//             "default": get_today_date()
//         },
//     ]
// };


// function get_date_30_days_ago() {
//     var date = new Date();
//     date.setDate(date.getDate() - 30); // Subtract 30 days from today
//     return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
// }

// // Function to get today's date
// function get_today_date() {
//     var date = new Date();
//     return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
// }



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
                // Filter Employee records if needed
                return {
                    filters: { designation: "Technician" }
                };
            },
            "default": get_default_technician()
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
    ]
};

function get_date_30_days_ago() {
    var date = new Date();
    date.setDate(date.getDate() - 30); // Subtract 30 days from today
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}

function get_today_date() {
    var date = new Date();
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}

// Function to set default Technician if the user has a Technician role
function get_default_technician() {
    var default_technician = null;
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Has Role",
            fields: ["parent"],
            filters: {
                role: "Technician",
                parenttype: "User",
                parent: frappe.session.user
            }
        },
        async: false,
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                // Fetch employee link from User-Employee connection if exists
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Employee",
                        fieldname: "name",
                        filters: {
                            user_id: frappe.session.user
                        }
                    },
                    async: false,
                    callback: function(res) {
                        if (res.message) {
                            default_technician = res.message.name;
                        }
                    }
                });
            }
        }
    });
    return default_technician;
}
