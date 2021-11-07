from __future__ import unicode_literals
import frappe
from frappe.utils.password import update_password

@frappe.whitelist()
def update_user_info():
    user = frappe.session.user
    fullname = frappe.form_dict.fullname
    email = frappe.form_dict.email
    pwd = frappe.form_dict.password
    if fullname and email:
        if pwd:
            update_password(user, pwd)
        name = frappe.db.get_value("User", {"email": email}, ["name"])
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

@frappe.whitelist()
def get_user_data():
    user = frappe.session.user
    return frappe.db.get_value("User", user, ["email", "full_name"], as_dict=True)

@frappe.whitelist()
def get_parent_data():
    user = frappe.session.user
    data = frappe.db.get_value("School Parent", user, ["contract_no", "branch", "year"], as_dict=True)
    students = frappe.db.sql("""
        SELECT student_no, student_name, class, section
        FROM `tabSchool Student`
        WHERE parent_no=%s
    """, user, as_dict=True)
    #frappe.db.get_list("School Student", filters = {"parent_no": user}, fields=["student_no", "student_name", "class", "section"])
    if data:
        data["students"] = students
    return data if data else {}