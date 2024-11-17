// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Collection", {
	refresh(frm) {
        calculate_payment_totals(frm)
        calculate_pending_payment_totals(frm);
        calculate_grand_total(frm)
	},
    
});

frappe.ui.form.on('Payments', {
    amount: function (frm) {
        console.log(frm);
        calculate_payment_totals(frm);
        calculate_grand_total(frm)
    }
});

frappe.ui.form.on('Pending Payments', {
    amount: function (frm) {
        console.log(frm);
        calculate_pending_payment_totals(frm);
        calculate_grand_total(frm)
    }
});



function calculate_grand_total(frm){
    var grand_total = frm.doc.total_payments_amount + frm.doc.total_pending_payment_amount
    frm.set_value("grand_total",grand_total)
}


function calculate_payment_totals(frm) {

    let total_amount = 0;
    var payments_tab = frm.doc.payments

    if (payments_tab && payments_tab.length > 0) {
        frm.doc.payments.forEach(row => {
            total_amount += row.amount || 0; 
        });
    }

    frm.set_value('total_payments_amount', total_amount);
}


function calculate_pending_payment_totals(frm) {

    let total_pending_amount = 0;
    var total_pending_payments = frm.doc.pending_payment_collection


    
    if (total_pending_payments && total_pending_payments.length > 0) {
        
        frm.doc.pending_payment_collection.forEach(row => {
            total_pending_amount += row.amount || 0; 
        });
    }

    frm.set_value('total_pending_payment_amount', total_pending_amount);
}
