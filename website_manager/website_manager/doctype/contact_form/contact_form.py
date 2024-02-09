# Copyright (c) 2024, Douglas Nkubitu and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document


class ContactForm(Document):
	pass

@frappe.whitelist()                
def get_contact_form_data(doc):
    contact_form_doc = frappe.get_doc("Contact Form", doc)
    return {
        'full_name': contact_form_doc.full_name,
        'email_address': contact_form_doc.email_address,
        'phone_number': contact_form_doc.phone_number,
        'company': contact_form_doc.company,
        'message': contact_form_doc.message
    }

@frappe.whitelist()
def get_email_template(template_name, doc, full_name=None, email_address=None, phone_number=None, company=None, message=None):
    """Returns the processed HTML of an email template with the given doc and additional fields"""
    if isinstance(doc, str):
        doc = json.loads(doc)

    email_template = frappe.get_doc("Email Template", template_name)
    if full_name:
        doc["full_name"] = full_name
    if email_address:
         doc["email_address"] = email_address
    if phone_number:
        doc["phone_number"] = phone_number
    if company:
        doc["company"] = company
    if message:
        doc["message"] = message

    return email_template.get_formatted_email(doc)

@frappe.whitelist()
def send_email(subject, content):
    default_email_account = frappe.get_doc("Email Account", {"default_outgoing": 1})

    # Check if a default email account is configured
    if not default_email_account:
        error_message = "Error: No default email account configured."
        frappe.log_error(error_message, "Default Email Account Error")
        return error_message

    frappe.sendmail(
        recipients=default_email_account.email_id,
        subject=subject,
        content=content
    )
