// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Maintenance Schedule Assignment", {
	get_schedules(frm) {
        var from_date = frm.doc.from_date
        var to_date = frm.doc.to_date

        frappe.call({
            method:'inverter.inverter.doctype.maintenance_schedule_assignment.maintenance_schedule_assignment.get_schedules',
            args:{
                from_date:from_date,
                to_date:to_date,
            },
            callback:function(r){
                console.log(r);
                var schedule_data = r.message

                frappe.model.clear_table(frm.doc, 'schedule_assignment');

                schedule_data.forEach(function(data){
                    console.log(data.parent);
                    frm.add_child("schedule_assignment",{
                        maintenance_schedule_id:data.parent,
                        item:data.item_code,
                        schedule_date:data.scheduled_date,
                        technician:data.custom_technician,
                        email_id:data.custom_technician_email,
                        email:data.custom_email,
                        id:data.name
                    })
                   
                })
                frm.refresh_field("schedule_assignment")
            }
        })
	},
    assign_schedule(frm){
        frappe.call({
            method:'inverter.inverter.doctype.maintenance_schedule_assignment.maintenance_schedule_assignment.assign_schedule',
            args:{
                name:frm.doc.name
            },
            callback:function(r){
                console.log(r);
                frm.reload_doc()
            }       
        })
    }
});

// Subscribe to real-time progress updates
frappe.realtime.on("email_sending_progress", (data) => {
    frappe.show_progress(data.title, (data.progress / data.total) * 100, data.description);

    // If progress reaches 100%, show a completion message
    if (data.progress === data.total) {
        frappe.show_progress(data.title, 100, "All emails sent successfully!");
        frappe.msgprint(__("All emails have been sent successfully!"));
    }
});