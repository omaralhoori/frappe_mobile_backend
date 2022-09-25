# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import threading
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend.notification import send_multiple_notification
from mobile_backend.mobile_backend.utils import get_current_site_name
from frappe.utils.dateutils import datetime
from frappe.desk.form.load import get_attachments
from mobile_backend.mobile_backend.doctype.school_messaging.school_messaging import add_attachment_file
import sys

class SchoolGroupMessage(Document):
	def on_submit(self):
		attachments = get_attachments(self.doctype, self.name)
		attachments_list = [attach.file_url for attach in attachments]
		kwargs = {
			"name":self.name,"title":self.title, "message":self.message, "branch":self.branch,
			"class_code":self.class_code, "section_code":self.section, "site": get_current_site_name(),
			"attachments": ";".join(attachments_list), "thumbnail": self.thumbnail
		}
		#add_group_message(**kwargs)
		thread = threading.Thread(target=add_group_message, kwargs=kwargs)
		thread.start()

	def on_trash(self):
		delete_group_message(self.name)

def delete_group_message(name):
	frappe.db.sql("""
	DELETE t1,t2 FROM `tabSchool Messaging` as t1
		INNER JOIN `tabSchool Messages` as t2 ON t1.name=t2.parent
		WHERE t1.message_name=%s AND t1.message_type='School Group Message'
	""", (name))
	frappe.db.commit()
# def delete_group_message(name):
# 	frappe.db.sql("""
# 		DELETE FROM `tabSchool Parent Message` WHERE message_name=%s AND message_type='Group Message'
# 	""", (name))
# 	frappe.db.commit()

def add_group_message(title, message, branch, name, site, class_code=None, section_code=None, attachments="", thumbnail=""):
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
			try:
				message_name = frappe.db.get_value("School Messaging", {
					"message_type": "School Group Message",
					"parent_name": student["parent_no"],
					"message_name": name
				}, "name")
				if not message_name:
					doc = frappe.get_doc({
						"doctype": "School Messaging",
						"parent_name": student["parent_no"],
						"student_no": student["student_no"],
						"student_name": student["student_name"],
						"title": title,
						"branch": branch,
						"message_name": name,
						"message_type": "School Group Message",
						"attachments": attachments,
						"thumbnail": thumbnail
					})
					row = doc.append("messages")
					row.sender_name = "Administration"
					row.message = message
					row.is_administration = 1
					row.sending_date = datetime.datetime.now()
					doc.insert()
					add_attachment_file("School Group Message", name, doc.name, "School Messaging")
					device_token = frappe.db.get_value("School Parent", student["parent_no"], ["device_token"])
					try:
						send_multiple_notification(device_token, title, message, {
							"type": "School Group Message",
							"student_no": student["student_no"],
							"name": doc.name
						})
					except BaseException as e:
						print(f"Unexpected {e=}, {type(e)=}, {student['parent_no']}")
					frappe.db.commit()
				else:
					# frappe.db.set_value("School Messaging", message_name, {
					# 	"title": title,
					# 	"message": message,
					# })
					doc = frappe.get_doc("School Messaging", message_name)
					doc.title = title
					doc.thumbnail = thumbnail
					doc.attachments = attachments
					add_attachment_file("School Group Message", name, doc.name, "School Messaging")
					for _message in doc.messages:
						if _message.is_administration == 1:
							_message.message = message
							break
					doc.save()
			except BaseException as err:
				print(f"Unexpected {err=}, {type(err)=}, {student['parent_no']}")
	frappe.db.commit()

