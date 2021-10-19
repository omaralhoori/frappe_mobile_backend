# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ContactMessages(Document):
	pass


@frappe.whitelist(allow_guest=True)
def send_message():
	sender_name = frappe.form_dict.sender_name
	email = frappe.form_dict.email
	subject = frappe.form_dict.subject
	message = frappe.form_dict.message
	frappe.get_doc({
		"doctype": "Contact Messages",
		"sender_name":sender_name,
		"email":email,
		"subject":subject,
		"message":message
	}).insert(ignore_permissions=True)