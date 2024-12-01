frappe.ui.form.on('Maintenance Visit', {

    setup: function (frm) {
        const current_user = frappe.session.user;

        // Call the whitelisted function
        frappe.call({
            method: "inverter.apis.maintenance_visit.get_technician_roles", // Replace `custom_app` with your app name
            args: {
                user: current_user
            },
            callback: function (response) {
                console.log(response);
                if (response.message.length > 0 &&
                    !frappe.user_roles.includes("System Manager") &&
                    frappe.user != "Administrator") {

                    // Set dynamic filter for the maintenance_schedule_detail field
                    frm.set_query('maintenance_schedule_detail', function () {
                        return {
                            filters: {
                                status: ["in", ["Pending", "Partially Completed"]],
                                "maintenance_schedule_details.employee": frappe.session.user
                            }
                        };
                    });
                }

            }
        });
    },
    refresh: function (frm) {
        set_serialno_filter(frm)
        // Check if the user is a Technician but not an Admin or System Manager
        if (
            frappe.user_roles.includes("Technician") &&
            !frappe.user_roles.includes("Administrator") &&
            !frappe.user_roles.includes("System Manager")
        ) {
            
            // Call the functions only for "Technician" role
            console.log(cur_frm.doc.docstatus !=1 && cur_frm.doc.docstatus!=2);
            if(cur_frm.doc.docstatus !=1 && cur_frm.doc.docstatus!=2)
               {
                get_schedules(frm);
               } 
        }



    },
    on_update: function(frm) {
        
        let current_time = new Date();
        let hours = current_time.getHours();
        let minutes = current_time.getMinutes();
        
        let time_string = (hours < 10 ? '0' : '') + hours + ':' + (minutes < 10 ? '0' : '') + minutes;
        
        frm.set_value('custom_time_field', time_string);
    },
    customer: function (frm) {
        set_serialno_filter(frm)
    }
});

function set_serialno_filter(frm) {
    if (frm.doc.customer) {
        frappe.call({
            method: 'inverter.apis.maintenance_visit.get_serial_no',
            args: {
                customer: frm.doc.customer
            },
            callback: function (r) {
                if (r.message) {
                    frm.fields_dict["purposes"].grid.get_field("serial_no").get_query = function () {
                        return {
                            filters: [
                                ["Serial No", "name", "in", r.message]
                            ]
                        };
                    };

                }
            }
        });
    }
}



// function get_schedules(frm) {
//     frm.add_custom_button(__('Select Maintenance Schedules'), function() {
//         // Call the server-side function to fetch the pending schedules
//         frappe.call({
//             method: "inverter.apis.maintenance_visit.get_pending_maintenance_schedules",  // Replace with the correct path
//             callback: function(r) {
//                 if (r.message) {
//                     console.log(r.message);
//                     // Create an array of options for the Select field
//                     let scheduleOptions = r.message.map(schedule => ({
//                         label: frappe.datetime.str_to_user(schedule.scheduled_date),  // Format the date to dd-mm-yyyy
//                         value: schedule.name       // This is the ID (name) that will be used in the background
//                     }));
//                     console.log(scheduleOptions);
//                     // Create the dialog with the fetched options
//                     let d = new frappe.ui.Dialog({
//                         title: 'Enter details',
//                         fields: [
//                             {
//                                 label: 'Schedule',
//                                 fieldname: 'schedule',
//                                 fieldtype: 'Select',
//                                 options: scheduleOptions  // Set the options dynamically
//                             },
//                         ],
//                         size: 'small', // small, large, extra-large 
//                         primary_action_label: 'Submit',
//                         primary_action(values) {
//                             console.log(values);
//                             d.hide();
//                         }
//                     });

//                     // Show the dialog
//                     d.show();
//                 }
//             }
//         });
//     });
// }



function get_schedules(frm) {
    frm.add_custom_button(__('Select Maintenance Schedules'), function () {
        // Call the server-side function to fetch the pending schedules
        frappe.call({
            method: "inverter.apis.maintenance_visit.get_pending_maintenance_schedules",  // Replace with the correct path
            callback: function (r) {
                if (r.message) {
                    console.log(r.message);
                    // Create an array of options for the Select field
                    let scheduleOptions = r.message.map(schedule => ({
                        label: frappe.datetime.str_to_user(schedule.scheduled_date),  // Format the date to dd-mm-yyyy
                        value: schedule.name       // This is the ID (name) that will be used in the background
                    }));
                    console.log(scheduleOptions);

                    // Create the dialog with the fetched options
                    let d = new frappe.ui.Dialog({
                        title: 'Enter details',
                        fields: [
                            {
                                label: 'Schedule',
                                fieldname: 'schedule',
                                fieldtype: 'Select',
                                options: scheduleOptions  // Set the options dynamically
                            },
                        ],
                        size: 'small', // small, large, extra-large 
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            // Log the selected schedule name (ID)
                            console.log('Selected Schedule:', values.schedule);

                            // Fetch parent document details based on selected schedule using the custom method
                            frappe.call({
                                method: "inverter.apis.maintenance_visit.get_maintenance_schedule_details",  // Custom method
                                args: {
                                    schedule_name: values.schedule  // The selected schedule name (ID)
                                },
                                callback: function (r) {
                                    if (r.message) {
                                        
                                        frappe.model.clear_table(frm.doc, 'purposes');
                                        // Access schedule details
                                        const scheduleDetail = r.message.schedule_detail;

                                        // Access parent maintenance schedule details
                                        const maintenanceSchedule = r.message.maintenance_schedule;

                                        // Set the 'maintenance_schedule' field with the 'name' from the maintenance_schedule
                                        frm.set_value('maintenance_schedule', maintenanceSchedule.name);

                                        // Set the 'customer' field with the 'customer' from the maintenance_schedule
                                        frm.set_value('customer', maintenanceSchedule.customer);
                                        frm.set_value("maintenance_type","Scheduled")
                                        frm.add_child("purposes", {
                                            item_code: scheduleDetail.item_code,
                                            item_name: scheduleDetail.item_name,
                                            custom_technician: scheduleDetail.custom_technician,
                                            prevdoc_doctype: "Maintenance Schedule Detail",
                                            prevdoc_docname: scheduleDetail.name,
                                            maintenance_schedule_detail: scheduleDetail.name
                                        })
                                        frm.refresh_field("purposes")

                                        // Optionally, you can log the values to check
                                        console.log('Maintenance Schedule Name:', maintenanceSchedule.name);
                                        console.log('Customer:', maintenanceSchedule.customer);
                                    }
                                }
                            });

                            d.hide();  // Hide the dialog after submit
                        }
                    });

                    // Show the dialog
                    d.show();
                }
            }
        });
    });
}


