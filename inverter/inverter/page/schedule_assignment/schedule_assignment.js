frappe.pages['schedule-assignment'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Schedule Assignment',
		single_column: true
	});
}