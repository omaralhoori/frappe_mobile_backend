from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def update_device_token():
    user = frappe.session.user
    token = frappe.form_dict.device_token
    frappe.db.set_value("School Parent", user, {"device_token":token})
    frappe.db.commit()