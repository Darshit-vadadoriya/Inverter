// frappe.listview_settings['Maintenance Visit'] = {
//     onload: function (listview) {
//         apply_default_filter(listview);
//     },
//     refresh: function (listview) {
//         apply_default_filter(listview);
//     }
// };

// function apply_default_filter(listview) {
//     if (frappe.user.has_role('Technician') &&
//         !frappe.user.has_role(['Administrator', 'System Manager'])) {
        
//         frappe.db.get_list('Employee', {
//             filters: { user_id: frappe.session.user },
//             fields: ['name']
//         }).then(employees => {
//             if (employees.length) {
//                 const employee_name = employees[0].name;

//                 frappe.call({
//                     method: 'inverter.apis.maintenance_visit.get_maintenance_visits_for_technician',
//                     args: { employee: employee_name },
//                     callback: function (r) {
//                         if (r.message) {
//                             // Add the filter directly using filter_area
//                             listview.filter_area.add([
//                                 ['Maintenance Visit', 'name', 'in', r.message]
//                             ]);

//                             // Refresh the list view
//                             listview.refresh();
//                         }
//                     }
//                 });
//             }
//         });
//     }
// }


// frappe.listview_settings['Maintenance Visit'] = {
//     onload: function (listview) {
//         apply_default_filter(listview);
//     },
//     refresh: function (listview) {
//         apply_default_filter(listview);
//     }
// };

// function apply_default_filter(listview) {
//     // Check if the user is a Technician but not an Admin, Administrator, or System Manager
//     if (
//         frappe.user.has_role('Technician') &&
//         !frappe.user.has_role(['Admin', 'Administrator', 'System Manager'])
//     ) {
//         frappe.db.get_list('Employee', {
//             filters: { user_id: frappe.session.user },
//             fields: ['name']
//         }).then(employees => {
//             // Clear existing filters to avoid conflicts
//             listview.filter_area.clear();

//             if (employees.length) {
//                 const employee_name = employees[0].name;

//                 frappe.call({
//                     method: 'inverter.apis.maintenance_visit.get_maintenance_visits_for_technician',
//                     args: { employee: employee_name },
//                     callback: function (r) {
//                         if (r.message && r.message.length > 0) {
//                             // Add filter to show only records linked to the employee
//                             listview.filter_area.add([
//                                 ['Maintenance Visit', 'name', 'in', r.message]
//                             ]);
//                         } else {
//                             // If no visits are found, show no data
//                             listview.filter_area.add([
//                                 ['Maintenance Visit', 'name', '=', '']
//                             ]);
//                         }
//                         listview.refresh();
//                     }
//                 });
//             } else {
//                 // If the user is not linked to any employee, show no data
//                 listview.filter_area.add([
//                     ['Maintenance Visit', 'name', '=', 'Rachana Power']
//                 ]);
//                 listview.refresh();
//             }
//         });
//     }
// }
 