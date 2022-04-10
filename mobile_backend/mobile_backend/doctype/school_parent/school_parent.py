# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SchoolParent(Document):
	def get_students(self):
		#students = []
		return frappe.db.get_list("School Student", {"parent_no": self.name}, ["student_no", "student_name", "class", "section"])




# @frappe.whitelist()
# def get_messages():
# 	messages = frappe.db.get_list("School Parent Message", 
# 	filters={"parent": frappe.session.user}, 
# 	fields=["title", "message", "creation","message_type", "student_name", "student_no", "message_name", "is_viewed"],
# 		order_by='creation desc',
# 	)
# 	return messages

# @frappe.whitelist()
# def view_message():
# 	message_name = frappe.form_dict.message_name
# 	frappe.db.set_value("School Parent Message",{
# 		"message_name": message_name,
# 		"parent": frappe.session.user
# 	}, {
# 		"is_viewed": 1
# 	})
# 	frappe.db.commit()