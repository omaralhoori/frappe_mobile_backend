from __future__ import unicode_literals
import frappe
from frappe import _

from frappe.utils import get_site_name

def get_or_create_user(user):
    if frappe.session.user == 'Guest' and user:
        res = frappe.db.get_value("Mobile Guest", user, ["name","is_active"])
        if res:
            name, is_active = res
            if is_active == 1:
                return name
            else: return frappe.throw("You are not allowed to use the system.")
        else:
            user_doc = frappe.get_doc({
                "doctype": "Mobile Guest",
                "device_id": user
            })
            user_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return user_doc.name
    else:
        return frappe.session.user




def get_current_site_name():
    return get_site_name(frappe.local.request.host)