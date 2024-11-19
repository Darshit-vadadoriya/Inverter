// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Area Wise Maintenance Schedule"] = {
	filters: [
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer",
        },
        {
            fieldname: "financial_year",
            label: __("Financial Year"),
            fieldtype: "Link",
            options: "Fiscal Year",
        },
		{
            fieldname: "locality",
            label: __("Locality"),
            fieldtype: "Link",
            options: "Locality",
        },
    ],
};
