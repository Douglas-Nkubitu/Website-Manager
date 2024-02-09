// Copyright (c) 2024, Douglas Nkubitu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contact Form', {
	after_save: function (frm) {
		// Fetch data from the contact form document for sending email
		frappe.call({
			method: 'website_manager.website_manager.doctype.contact_form.contact_form.get_contact_form_data',
			args: {
                doc_name: frm.doc.name,
			},
			callback: function(response) {
				if (response && response.message) {
					// Fetch data from contact form
					var full_name = response.message.full_name;
                    var email_address = response.message.email_address;
                    var phone_number = response.message.phone_number;
                    var company = response.message.company;
                    var message = response.message.message;

					frappe.call({
						method: 'website_manager.website_manager.doctype.contact_form.contact_form.get_email_template',
						args: {
							template_name: 'New Inquiry',
							doc: frm.doc,
							full_name: full_name,
                            email_address: email_address,
                            phone_number: phone_number,
                            company: company,
                            message: message,
						},
						callback: function(emailResponse) {
							if (emailResponse && emailResponse.message) {
								// Fetch email message from response
								var message = emailResponse.message;

								// Send the email
								frappe.call({
									method: 'website_manager.website_manager.doctype.contact_form.contact_form.send_email',
									args: {
										subject: message.subject,
										content: message.message
									},
									callback: function(r) {
										if (r.exc) {
											msgprint(r.exc);
											return;
										}
									}
								});
							}
						}
					});
				}
			}
		});
	}
})