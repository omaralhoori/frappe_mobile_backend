# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import date
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend.utils import get_current_site_name
from mobile_backend.mobile_backend.notification import send_token_notification
from frappe.utils.dateutils import datetime

class SchoolDirectMessage(Document):
	def on_update(self):
		add_direct_message(self.title, self.message, self.branch, self.year, self.contract, self.name, get_current_site_name())

	def on_trash(self):
		delete_direct_message(self.name)


def delete_direct_message(name):
	frappe.db.sql("""
		DELETE t1,t2 FROM `tabSchool Messaging` as t1
		INNER JOIN `tabSchool Messages` as t2 ON t1.name=t2.parent
		WHERE t1.message_name=%s AND t1.message_type='School Direct Message'
	""", (name))
	frappe.db.commit()
# def delete_direct_message(name):
# 	frappe.db.sql("""
# 		DELETE FROM `tabSchool Parent Message` WHERE message_name=%s AND message_type='Direct Message'
# 	""", (name))
# 	frappe.db.commit()

def add_direct_message(title, message, branch, year, contract , name, site):
	filters = {
		"branch": branch,
		"year": year,
		"contract_no": contract
	}
	parent_value = frappe.db.get_value('School Parent', filters, ["name", "device_token"])
	if parent_value:
		parent_name, device_token = parent_value
		if parent_name:
			message_name = frappe.db.get_value("School Messaging", {
				"parent_name": parent_name,
				"message_name": name,
				"message_type": "School Direct Message"
			}, "name")
			if not message_name:
				doc = frappe.get_doc({
					"doctype": "School Messaging",
					"parent_name": parent_name,
					"title": title,
					"message_name": name,
					"branch": branch,
					"message_type": "School Direct Message"
				})
				row = doc.append("messages")
				row.sender_name = "Administration"
				row.message = message
				row.is_administration = 1
				row.sending_date = datetime.datetime.now()
				doc.insert()
				send_token_notification(device_token, title, message, {
					"message_type": "School Direct Message",
					"message_name": name
				})
			else:
				doc = frappe.get_doc("School Messaging", message_name)
				doc.title = title
				for _message in doc.messages:
					if _message.is_administration == 1:
						_message.message = message
						break
				doc.save()
	frappe.db.commit()

def add_replay(message_name, message):
	pass

"""
message_name = frappe.db.get_value("School Parent Message", {
				"parenttype": "School Parent",
				"parent": parent_name,
				"message_name": name
			}, "name")
			if not message_name:
				frappe.get_doc({
					"doctype": "School Parent Message",
					"parenttype": "School Parent",
					"parent": parent_name,
					"parentfield": "messages",
					"title": title,
					"message": message,
					"student": "0",
					"message_name": name,
					"message_type": "Direct Message"
				}).insert()

				send_token_notification(device_token, title, message)
			else:
				frappe.db.set_value("School Parent Message", message_name, {
					"title": title,
					"message": message,
				})
"""