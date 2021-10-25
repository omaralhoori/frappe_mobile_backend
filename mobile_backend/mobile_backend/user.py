from __future__ import unicode_literals
import frappe


@frappe.whitelist()
def update_user_info():
    user = frappe.session.user
    fullname = frappe.form_dict.fullname
    email = frappe.form_dict.email
    if fullname and email:
        name = frappe.db.get_value("User", {"email": email}, ["name"])
        print(name)
        if not name or name == user:
            frappe.db.set_value("User", user, {
                "email": email,
                "full_name": fullname,
                "first_name": fullname
            })
            frappe.db.commit()
        else:
            return {
                "error": "Email is in use!"
            }