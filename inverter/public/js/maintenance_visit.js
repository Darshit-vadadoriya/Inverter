frappe.ui.form.on('Maintenance Visit', {
    refresh:function(frm){
       set_serialno_filter(frm) 
    },
    customer: function (frm) {
       set_serialno_filter(frm)
    }
});

function set_serialno_filter(frm){
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