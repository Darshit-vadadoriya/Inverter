// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Maintenance Visit Done Area Wise"] = {
	filters: [
        {
            fieldname: "financial_year",
            label: __("Financial Year"),
            fieldtype: "Link",
            options: "Fiscal Year",
        },
		{
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default:frappe.defaults.get_default("company")
        },
        {
            fieldname: "product_group",
            label: __("Product Group"),
            fieldtype: "Link",
            options: "Product Group",
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
