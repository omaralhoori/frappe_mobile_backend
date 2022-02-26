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
            return {
                "message": "Profile updated successfully"
            }
        else:
            return {
                "error": "Email is in use!"
            }

@frappe.whitelist()
def update_user_pwd():
    user = frappe.form_dict.user
    pwd = frappe.form_dict.password
    update_password(user, pwd)

@frappe.whitelist()
def get_user_data():
    user = frappe.session.user
    return frappe.db.get_value("User", user, ["email", "full_name", "user_image"], as_dict=True)

@frappe.whitelist()
def get_parent_data():
    user = frappe.session.user
    data = frappe.db.sql("""
        SELECT p.contract_no, b.branch_code, b.branch_name, y.year_name FROM `tabSchool Parent` as p
        INNER JOIN `tabSchool Branch` as b ON p.branch=b.name
        INNER JOIN `tabSchool Year` as y ON p.year=y.name
        WHERE p.name=%s
    """, user, as_dict=True)
    #frappe.db.get_value("School Parent", user, ["contract_no", "branch", "year"], as_dict=True)
    students = frappe.db.sql("""
        SELECT s.student_no, s.student_name, c.class_code, c.class_name, se.section_code, se.section_name, IFNULL(s.student_gender, 'Male')
        FROM `tabSchool Student` as s
        INNER JOIN `tabSchool Class` as c ON s.class=c.name
        INNER JOIN `tabSchool Section` as se ON s.section=se.name
        WHERE parent_no=%s
    """, user, as_dict=True)
    #frappe.db.get_list("School Student", filters = {"parent_no": user}, fields=["student_no", "student_name", "class", "section"])
    if len(data) > 0:
        data = data[0]
        data["students"] = students
    return data if data else {}


@frappe.whitelist()
def get_user_type():
    user = frappe.session.user
    teacher = frappe.db.get_value("School Teacher", user, ["name"])
    parent = frappe.db.get_value("School Parent", user, ["name"])
    return {
        "parent": True if parent else False,
        "teacher": True if teacher else False
    }