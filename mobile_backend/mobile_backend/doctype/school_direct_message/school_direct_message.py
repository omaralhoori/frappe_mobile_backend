# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend.utils import get_current_site_name
from mobile_backend.mobile_backend.notification import send_parent_notification

class SchoolDirectMessage(Document):
	def on_update(self):
		add_direct_message(self.title, self.message, self.branch, self.year, self.contract, self.name, get_current_site_name())

	def on_trash(self):
		delete_direct_message(self.name)


def delete_direct_message(name):
	frappe.db.sql("""
		DELETE FROM `tabSchool Parent Message` WHERE message_name=%s AND message_type='Direct Message'
	""", (name))
	frappe.db.commit()

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

				send_parent_notification(device_token, title, message)
			else:
				frappe.db.set_value("School Parent Message", message_name, {
					"title": title,
					"message": message,
				})
	frappe.db.commit()

