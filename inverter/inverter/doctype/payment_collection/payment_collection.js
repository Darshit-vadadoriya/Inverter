// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Collection", {
	refresh(frm) {
        calculate_payment_totals(frm)
        calculate_pending_payment_totals(frm);
        calculate_grand_total(frm)
        set_selled_item_filter(frm)



        // Attach a custom click handler to the "payment_completion_proof" field
        frm.fields_dict['payment_completion_proof'].df.on_click = function () {
            // Open file uploader with camera directly
            frappe.ui.FileUploader.show({
                doctype: frm.doc.doctype,
                docname: frm.doc.name,
                fieldname: 'payment_completion_proof',
                options: {
                    accept: 'image/*', // Only allow images
                    capture: 'camera', // Open camera directly
                },
                callback: function (file) {
                    if (file && file.file_url) {
                        // Set the uploaded file's URL in the field
                        frm.set_value('payment_completion_proof', file.file_url);
                        frm.refresh_field('payment_completion_proof');
                        frappe.msgprint(__('Image uploaded successfully.'));
                    } else {
                        frappe.msgprint(__('Failed to upload the image.'));
                    }
                }
            });
        };

        // Refresh the field to apply changes
        frm.refresh_field('payment_completion_proof');
    



	},
    customer:function(frm){
        set_selled_item_filter(frm)

        get_outstanding(frm)

    },
    // payment_completion_proof: function (frm) {
    //     // Get the attach image field
    //     const image_field = frm.fields_dict['payment_completion_proof'];
        
    //     // Open the file uploader
    //     frappe.ui.FileUploader.show({
    //         doctype: frm.doc.doctype,
    //         docname: frm.doc.name,
    //         fieldname: 'payment_completion_proof',
    //         options: {
    //             accept: 'payment_completion_proof/*', // Only accept image files
    //             capture: 'camera' // Suggest opening the camera
    //         },
    //         callback: function (file) {
    //             // Set the image URL after uploading
    //             frm.set_value('payment_completion_proof', file.file_url);
    //             frm.refresh_field('payment_completion_proof');
    //         }
    //     });
    // }

   
    
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

// get selled item filter
function set_selled_item_filter(frm){
    if (frm.doc.customer) {
           frappe.call({
               method: 'inverter.inverter.doctype.payment_collection.payment_collection.get_unique_sold_items_by_customer',
               args: {
                   customer: frm.doc.customer
               },
               callback: function (r) {
                   if (r.message) {
                       frm.fields_dict["payments"].grid.get_field("item_code").get_query = function () {
                           return {
                               filters: [
                                   ["Item", "name", "in", r.message]
                               ]
                           };
                       };
       
                   }
               }
           });
       }
}


function get_outstanding(frm){
    frappe.call({
        method: "inverter.inverter.doctype.payment_collection.payment_collection.get_customer_outstanding",
        args: {
            customer: frm.doc.customer
        },
        callback: function(response) {
            if (response.message) {
                console.log(response.message);
                frm.set_value("outstanding_amount",response.message)
            }
        }
    });
}