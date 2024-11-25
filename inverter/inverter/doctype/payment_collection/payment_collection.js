// Copyright (c) 2024, Sahil Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payment Collection", {
	refresh(frm) {
        calculate_payment_totals(frm)
        calculate_pending_payment_totals(frm);
        calculate_grand_total(frm)
        set_selled_item_filter(frm)


        // frm.add_custom_button(__('Open Camera'), function() {
        //     // Create an invisible file input element
        //     var input = document.createElement('input');
        //     input.type = 'file';
        //     input.accept = 'image/*';
        //     input.capture = 'camera'; // This will trigger the camera dialog

        //     // Listen for the file selection event (image capture)
        //     input.onchange = function(event) {
        //         var file = event.target.files[0];  // Get the captured image file
                
        //         if (file) {
        //             var reader = new FileReader();
                    
        //             reader.onloadend = function() {
        //                 // The image data URL from the file reader
        //                 var imageData = reader.result;

        //                 // Set the image in the form's image field
        //                 frm.set_value('payment_completion_proof', imageData);
        //                 frm.refresh_field('payment_completion_proof');
        //             };

        //             // Read the file as a data URL (base64 encoded image)
        //             reader.readAsDataURL(file);
        //         }
        //     };

        //     // Trigger the file input dialog to open the camera
        //     input.click();
        // });


        // frm.add_custom_button(__('Capture and Upload Image'), function () {
        //     // Create an input element for capturing an image
        //     const input = document.createElement('input');
        //     input.type = 'file';
        //     input.accept = 'image/*';
        //     input.capture = 'environment'; // Prefer rear-facing camera
        
        //     input.onchange = function (event) {
        //         const file = event.target.files[0];
        //         if (file) {
        //             const formData = new FormData();
        //             formData.append('file', file);
        
        //             // Show loader during upload
        //             frappe.show_alert({ message: __('Uploading image...'), indicator: 'orange' });
        
        //             // Upload the image using fetch API
        //             fetch('/api/method/inverter.inverter.doctype.payment_collection.payment_collection.upload_image', {
        //                 method: 'POST',
        //                 headers: {
        //                     'X-Frappe-CSRF-Token': frappe.csrf_token
        //                 },
        //                 body: formData
        //             })
        //             .then(response => response.json())
        //             .then(data => {
        //                 if (data.message?.file_url) {
        //                     frm.set_value('payment_completion_proof', data.message.file_url);
        //                     frm.refresh_field('payment_completion_proof');
        //                     frm.save();
        //                 } else {
        //                     frappe.msgprint(__('Image upload failed.'));
        //                 }
        //             })
        //             .catch(error => {
        //                 console.error('Error:', error);
        //                 frappe.msgprint(__('Failed to upload the image.'));
        //             });
        //         }
        //     };
        
        //     // Open camera or file selector
        //     input.click();
        // });
        

	},
    upload_image(frm){
          // Create an input element for capturing an image
          const input = document.createElement('input');
          input.type = 'file';
          input.accept = 'image/*';
          input.capture = 'environment'; // Prefer rear-facing camera
      
          input.onchange = function (event) {
              const file = event.target.files[0];
              if (file) {
                  const formData = new FormData();
                  formData.append('file', file);
      
                  // Show loader during upload
                  frappe.show_alert({ message: __('Uploading image...'), indicator: 'orange' });
      
                  // Upload the image using fetch API
                  fetch('/api/method/inverter.inverter.doctype.payment_collection.payment_collection.upload_image', {
                      method: 'POST',
                      headers: {
                          'X-Frappe-CSRF-Token': frappe.csrf_token
                      },
                      body: formData
                  })
                  .then(response => response.json())
                  .then(data => {
                      if (data.message?.file_url) {
                          frm.set_value('payment_completion_proof', data.message.file_url);
                          frm.refresh_field('payment_completion_proof');
                          frm.save();
                      } else {
                          frappe.msgprint(__('Image upload failed.'));
                      }
                  })
                  .catch(error => {
                      console.error('Error:', error);
                      frappe.msgprint(__('Failed to upload the image.'));
                  });
              }
          };
      
          // Open camera or file selector
          input.click();
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



