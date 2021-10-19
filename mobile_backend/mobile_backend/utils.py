from __future__ import unicode_literals
import frappe

def get_or_create_user(user):
    return user if user else frappe.session.user