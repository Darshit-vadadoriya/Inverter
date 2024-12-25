// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Assign Maintenance Schedule", {
// 	refresh(frm) {

// 	},
// });



frappe.ui.form.on("Assign Maintenance Schedule", {
    locality: function(frm) {
        // Also trigger filtering when the locality is changed programmatically
        filter_child_table_rows_by_locality(frm);
    },
    month:function(frm){
        filter_child_table_rows_by_locality(frm)
    },

	get_schedules(frm) {
        var from_date = frm.doc.from_date
        var to_date = frm.doc.to_date

        frappe.call({
            method:'inverter.inverter.doctype.assign_maintenance_schedule.assign_maintenance_schedule.get_schedules',
            args:{
                from_date:from_date,
                to_date:to_date,
            },
            callback:function(r){
                console.log(r);
                
                var msg_length = r.message.length
                if(msg_length == 0){
                    frappe.msgprint("Schedule is not available on this date.")
                }
                var schedule_data = r.message

                frappe.model.clear_table(frm.doc, 'schedule_assignment');

                schedule_data.forEach(function(data){
                    
                    frm.add_child("schedule_assignment",{
                        maintenance_schedule_id:data.maintenance_schedule,
                        item:data.item_code,
                        schedule_date:data.scheduled_date,
                        technician:data.custom_technician,
                        email_id:data.custom_technician_email,
                        email:data.custom_email,
                        customer:data.customer,
                        outstandingamount:data.outstandingamount,
                        locality:data.custom_locality,
                        id:data.name
                    })
                   
                })
                frm.refresh_field("schedule_assignment")
            }
        })
    },
    

    refresh: function(frm) {
       
        $("[data-label='Submit']").click(function() {
            // Initialize an array to store unique customer-wise outstanding amounts
            var customer_outstanding = [];
        
            // Keep track of customers already added to avoid duplicates
            var added_customers = {};
        
            // Loop through the rows in the 'schedule_assignment' child table
            frm.doc.schedule_assignment.forEach(function(row) {
                if (row.customer && row.outstandingamount) {  // Check if the row has customer and outstandingamount
                    if (!added_customers[row.customer]) { // If the customer is not already added
                        customer_outstanding.push({
                            customer: row.customer,
                            outstandingamount: row.outstandingamount
                        });
                        added_customers[row.customer] = true; // Mark the customer as added
                    }
                }
            });
        
            // Prepare the message to display the customer-wise outstanding amounts with a table
            var outstanding_message = `
                <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
                    <thead>
                        <tr style="background-color: #f1f1f1;">
                            <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">No</th>
                            <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Customer Name</th>
                            <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">Outstanding Amount</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
        
            customer_outstanding.forEach(function(item, index) {
                outstanding_message += `
                    <tr>
                        <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${index + 1}</td>
                        <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${item.customer}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">${frappe.format(item.outstandingamount, {fieldtype: 'Currency'})}</td>
                    </tr>
                `;
            });
        
            outstanding_message += `
                    </tbody>
                </table>
                <br>
                <b>Are you sure you want to submit this document?</b>
            `;
        
            console.log(outstanding_message);
        
            // Update the modal body with the outstanding message
            setTimeout(() => {
                $(".modal-body").html(outstanding_message);
            }, 150);
        });
        
    
     
    
    },


});





// Function to filter child table rows based on locality and month
function filter_child_table_rows_by_locality(frm) {
    const selected_locality = frm.doc.locality || ""; // Get the selected locality
    const selected_month = frm.doc.month || ""; // Get the selected month (e.g., "January", "February")

    // Map month names to their respective numbers (1 = January, 2 = February, etc.)
    const month_map = {
        January: 1,
        February: 2,
        March: 3,
        April: 4,
        May: 5,
        June: 6,
        July: 7,
        August: 8,
        September: 9,
        October: 10,
        November: 11,
        December: 12
    };

    const month_number = month_map[selected_month] || null; // Convert the selected month to a number

    // Ensure child table data exists
    if (!frm.fields_dict.schedule_assignment || !frm.fields_dict.schedule_assignment.grid) {
        console.warn("Child table 'schedule_assignment' is not found.");
        return;
    }

    // Loop through child table rows
    frm.fields_dict.schedule_assignment.grid.data.forEach((row, idx) => {
        const row_locality = row.locality || ""; // Get the locality in the row
        const row_date = row.schedule_date || ""; // Get the schedule_date in the row
        const row_month = row_date ? new Date(row_date).getMonth() + 1 : null; // Extract the month from schedule_date

        // Check if the row matches the filters
        const locality_match = !selected_locality || row_locality === selected_locality;
        const month_match = !month_number || row_month === month_number;

        const should_show = locality_match && month_match;

        // Show or hide the row
        const grid_row = frm.fields_dict.schedule_assignment.grid.get_row(idx);
        if (grid_row) {
            $(grid_row.wrapper).toggle(should_show); // Show or hide the row
        }
    });

    // Refresh the grid to reflect changes
    frm.fields_dict.schedule_assignment.grid.refresh();
}
