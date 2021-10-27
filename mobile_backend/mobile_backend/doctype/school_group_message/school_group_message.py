# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import threading
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend.notification import send_parent_notification
from mobile_backend.mobile_backend.utils import get_current_site_name


class SchoolGroupMessage(Document):
	def on_update(self):
		kwargs = {
			"name":self.name,"title":self.title, "message":self.message, "branch":self.branch,
			"class_code":self.class_code, "section_code":self.section, "site": get_current_site_name()
		}
		thread = threading.Thread(target=add_group_message, kwargs=kwargs)
		thread.start()

	def on_trash(self):
		delete_group_message(self.name)

def delete_group_message(name):
	frappe.db.sql("""
		DELETE FROM `tabSchool Parent Message` WHERE message_name=%s AND message_type='Group Message'
	""", (name))
	frappe.db.commit()

def add_group_message(title, message, branch, name, site, class_code=None, section_code=None):
	frappe.init(site=site)
	frappe.connect()
	filters = {
		"branch": branch
	}
	if class_code:
		filters["class"] = class_code
		if section_code:
			filters["section"] = section_code
	students = frappe.db.get_list('School Student', filters=filters,fields=["name", "parent_no", "student_name", "student_no"])
	for student in students:
		if student["parent_no"]:
			message_name = frappe.db.get_value("School Parent Message", {
				"parenttype": "School Parent",
				"parent": student["parent_no"],
				"message_name": name
			}, "name")
			if not message_name:
				frappe.get_doc({
					"doctype": "School Parent Message",
					"parenttype": "School Parent",
					"parent": student["parent_no"],
					"parentfield": "messages",
					"student_no": student["student_no"],
					"student_name": student["student_name"],
					"student": student["name"],
					"title": title,
					"message": message,
					"message_name": name,
					"message_type": "Group Message"
				}).insert()

				device_token = frappe.db.get_value("School Parent", student["parent_no"], ["device_token"])
				send_parent_notification(device_token, title, message)
			else:
				frappe.db.set_value("School Parent Message", message_name, {
					"title": title,
					"message": message,
				})
	frappe.db.commit()

