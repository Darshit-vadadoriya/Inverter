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
                        outstanding_amount:data.outstanding_amount,
                        locality:data.custom_locality,
                        id:data.name
                    })
                   
                })
                frm.refresh_field("schedule_assignment")
            }
        })
    },
    
    // before_submit: function(frm) {
    //     // Initialize an empty object to store customer-wise outstanding amounts
    //     var customer_outstanding = {};
    
    //     // Loop through the rows in the 'schedule_assignment' child table
    //     frm.doc.schedule_assignment.forEach(function(row) {
    //         if (row.customer && row.outstanding_amount) {  // Check if the row has customer and outstanding_amount
    //             if (!customer_outstanding[row.customer]) {
    //                 customer_outstanding[row.customer] = 0;  // Initialize the customer if not already present
    //             }
    //             customer_outstanding[row.customer] += row.outstanding_amount;  // Add the outstanding amount to the customer
    //         }
    //     });
    
    //     // Prepare the message to display the customer-wise outstanding amounts with a table
    //     var outstanding_message = `
    //         <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
    //             <thead>
    //                 <tr style="background-color: #f1f1f1;">
    //                     <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">No</th>
    //                     <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Customer Name</th>
    //                     <th style="padding: 8px; text-align: right; border: 1px solid #ddd;">Outstanding Amount</th>
    //                 </tr>
    //             </thead>
    //             <tbody>
    //     `;
    
    //     var index = 1;
    //     for (var customer in customer_outstanding) {
    //         if (customer_outstanding.hasOwnProperty(customer)) {
    //             outstanding_message += `
    //                 <tr>
    //                     <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${index}</td>
    //                     <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${customer}</td>
    //                     <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">${frappe.format(customer_outstanding[customer], {fieldtype: 'Currency'})}</td>
    //                 </tr>
    //             `;
    //             index++;
    //         }
    //     }
    
    //     outstanding_message += `
    //             </tbody>
    //         </table>
    //     `;
    
    //     // Create and show the dialog box with the customer-wise outstanding amounts
    //     var dialog = new frappe.ui.Dialog({
    //         title: "Customer Wise Outstanding Amounts",
    //         fields: [
    //             {
    //                 fieldtype: 'HTML',
    //                 fieldname: 'outstanding_message',
    //                 options: outstanding_message
    //             }
    //         ],
    //         primary_action: function() {
    //             dialog.hide();
    //         },
    //         primary_action_label: 'Close'
    //     });
    
    //     dialog.show();
    
    // },



    refresh: function(frm) {
        $("[data-label='Submit']").click(function(){
            console.log("Hello===============")
        
            // Initialize an empty object to store customer-wise outstanding amounts
            var customer_outstanding = {};
        
            // Loop through the rows in the 'schedule_assignment' child table
            frm.doc.schedule_assignment.forEach(function(row) {
                if (row.customer && row.outstanding_amount) {  // Check if the row has customer and outstanding_amount
                    if (!customer_outstanding[row.customer]) {
                        customer_outstanding[row.customer] = 0;  // Initialize the customer if not already present
                    }
                    customer_outstanding[row.customer] += row.outstanding_amount;  // Add the outstanding amount to the customer
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
        
            var index = 1;
            for (var customer in customer_outstanding) {
                if (customer_outstanding.hasOwnProperty(customer)) {
                    outstanding_message += `
                        <tr>
                            <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${index}</td>
                            <td style="padding: 8px; text-align: left; border: 1px solid #ddd;">${customer}</td>
                            <td style="padding: 8px; text-align: right; border: 1px solid #ddd;">${frappe.format(customer_outstanding[customer], {fieldtype: 'Currency'})}</td>
                        </tr>
                    `;
                    index++;
                }
            }
        
            outstanding_message += `
                    </tbody>
                </table>

                <br>
                <b>Are you sure you want to submit this document?</b>
            `;

            console.log(outstanding_message);
           setTimeout(() => {
            $(".modal-body").html(outstanding_message)
           }, 150);
        })
    
     
    
    },


});














// // Function to filter child table rows based on the locality field
// function filter_child_table_rows_by_locality(frm) {
//     // Get the selected locality from the parent form
//     const selected_locality = frm.doc.locality;

//     // Loop through all rows in the child table
//     frm.fields_dict['schedule_assignment'].grid.wrapper.find('.grid-row').each(function() {
//         const row = $(this);

//         // Get the locality value from the child table row
//         const row_locality = row.find('[data-fieldname="locality"]').text();

//         // Show or hide the row based on the match
//         if (row_locality === selected_locality || !selected_locality) {
//             row.show(); // Show row if it matches or no locality is selected
//         } else {
//             row.hide(); // Hide row if it doesn't match
//         }
//     });
// }



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
