frappe.listview_settings['Maintenance Visit'] = {
    onload: function (listview) {
        apply_default_filter(listview);
    },
    refresh: function (listview) {
        apply_default_filter(listview);
    }
};

function apply_default_filter(listview) {
    if (frappe.user.has_role('Technician') &&
        !frappe.user.has_role(['Administrator', 'System Manager'])) {
        
        frappe.db.get_list('Employee', {
            filters: { user_id: frappe.session.user },
            fields: ['name']
        }).then(employees => {
            if (employees.length) {
                const employee_name = employees[0].name;

                frappe.call({
                    method: 'inverter.apis.maintenance_visit.get_maintenance_visits_for_technician',
                    args: { employee: employee_name },
                    callback: function (r) {
                        if (r.message) {
                            // Add the filter directly using filter_area
                            listview.filter_area.add([
                                ['Maintenance Visit', 'name', 'in', r.message]
                            ]);

                            // Refresh the list view
                            listview.refresh();
                        }
                    }
                });
            }
        });
    }
}
