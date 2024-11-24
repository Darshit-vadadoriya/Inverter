// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Area Wise Maintenance Pending Schedule"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_default("company")
        },
        {
            "fieldname": "customer",
            "label": "Customer",
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "custom_locality",
            "label": "Locality",
            "fieldtype": "Link",
            "options": "Locality"
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": get_date_30_days_ago() // Dynamically set the from_date as 30 days ago
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": get_today_date() // Dynamically set the to_date as today
        },
        {
            "fieldname": "financial_year",
            "label": "Financial Year",
            "fieldtype": "Link",
            "options": "Fiscal Year"
        }
    ],

    onload: function(report) {
       
        // Set the default financial year dynamically
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();
        const currentMonth = currentDate.getMonth() + 1;

        // Get the last date of the current month
        const lastDayOfMonth = new Date(currentYear, currentMonth, 0).getDate();  // 0 gives the last day of the previous month

        const currentMonthStr = currentMonth < 10 ? '0' + currentMonth : currentMonth;
        const lastDateStr = `${currentYear}-${currentMonthStr}-${lastDayOfMonth}`;

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Fiscal Year",
                fields: ["name"],
                filters: [
                    ["year_start_date", "<=", `${currentYear}-${currentMonthStr}-01`],
                    ["year_end_date", ">=", lastDateStr]
                ],
                limit_page_length: 1
            },
            callback: function(response) {

                
                if (response.message && response.message.length > 0) {
                    const financialYear = response.message[0].name;
                        console.log(financialYear);
                        report.set_filter_value('financial_year', financialYear);

                    // Ensure the filter value is updated after the response
                    report.refresh_filters();
                }
            }
        });
    }

};

// Function to get the date 30 days ago
function get_date_30_days_ago() {
    var date = new Date();
    date.setDate(date.getDate() - 30); // Subtract 30 days from today
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}

// Function to get today's date
function get_today_date() {
    var date = new Date();
    return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
}