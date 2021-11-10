# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.dateutils import datetime
class SchoolMessaging(Document):
	def get_messages(self):
		# messages = []
		# for message in self.messages:
		# 	messages.append({
		# 		"name": message.name,
		# 		"message": message.message,
		# 		"sender_name": message.sender_name,
		# 		"sending_date": message.sending_date,
		# 		"is_read": message.is_read,
		# 		"is_administration": message.is_administration
		# 	})
		messages = frappe.db.sql("""
		SELECT name, message, sender_name, sending_date, is_read, is_administration
		FROM `tabSchool Messages` WHERE parent=%s AND parenttype="School Messaging"
		""", (self.name), as_dict=True)
		return messages


@frappe.whitelist()
def get_messages():
	messages = frappe.db.sql("""
		SELECT name, title, creation, message_type, message_name, student_no, student_name
		FROM `tabSchool Messaging`
		WHERE parent_name=%s
		ORDER BY creation DESC
	""", frappe.session.user, as_dict=True)
	for message in messages:
		doc = frappe.get_doc("School Messaging", message["name"])
		message["messages"] = doc.get_messages() if doc else []
	return messages


@frappe.whitelist()
def add_reply():
	message_name = frappe.form_dict.message_name
	reply = frappe.form_dict.reply
	doc = frappe.get_doc("School Messaging", message_name)
	if doc:
		if doc.parent_name != frappe.session.user:
			return "You are not allowed to add reply to this message"
		rec = doc.append("messages")
		rec.message = reply
		rec.sender_name = frappe.db.get_value("User", frappe.session.user, "full_name")
		rec.sending_date = datetime.datetime.now()
		doc.status = 'Not seen'
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return {
			"name": rec.name
		}

@frappe.whitelist()
def delete_reply():
	message_name = frappe.form_dict.message_name
	reply_name = frappe.form_dict.reply_name
	doc = frappe.get_doc("School Messaging", message_name)
	if doc:
		if doc.parent_name != frappe.session.user:
			return "You are not allowed to delete this message"
		frappe.db.sql("""
		DELETE FROM `tabSchool Messages` WHERE name=%s AND parent=%s AND is_administration=0
		""", (reply_name, message_name))
		frappe.db.commit()

@frappe.whitelist()
def delete_replies():
	message_name = frappe.form_dict.message_name
	replies = frappe.form_dict.replies
	# for t in replies.keys():
	# 	reply_names += "'{}',".format(t)
	# reply_names = reply_names[:-1]
	doc = frappe.get_doc("School Messaging", message_name)
	if doc:
		if doc.parent_name != frappe.session.user:
			frappe.local.response['http_status_code'] = 403
			return "You are not allowed to delete this message"
		frappe.db.sql("""
		DELETE FROM `tabSchool Messages` WHERE name IN ({}) AND parent=%s AND is_administration=0
		""".format(replies), (message_name))
		frappe.db.commit()
	else:
		frappe.local.response['http_status_code'] = 404

@frappe.whitelist()
def view_message():
	message_name = frappe.form_dict.message_name
	doc = frappe.get_doc("School Messaging", message_name)
	if doc:
		if doc.parent_name != frappe.session.user:
			return "You are not allowed to add reply to this message"
		for message in doc.messages:
			if message.is_administration == 1:
				message.is_read = 1
		doc.save(ignore_permissions=True)
		frappe.db.commit()

		
# @frappe.whitelist()
# def get_messages2():
# 	messages = frappe.db.sql("""
# 		SELECT t.name, t.title, t.message_type, t.message_name, t.creation,
# 		GROUP_CONCAT(m.message ORDER BY m.sending_date ASC SEPARATOR '/;') as messages, 
# 		GROUP_CONCAT(m.sender_name ORDER BY m.sending_date ASC SEPARATOR '/;') as senders, 
# 		GROUP_CONCAT(m.is_read ORDER BY m.sending_date ASC SEPARATOR '/;') as is_reads, 
# 		GROUP_CONCAT(m.is_administration ORDER BY m.sending_date ASC SEPARATOR '/;') as is_administration, 
# 		GROUP_CONCAT(m.name ORDER BY m.sending_date ASC SEPARATOR '/;') as names, 
# 		GROUP_CONCAT(m.sending_date ORDER BY m.sending_date ASC SEPARATOR '/;') as creations 
# 		FROM `tabSchool Messaging` as t
# 		LEFT JOIN `tabSchool Messages` as m on t.name=m.parent
# 		WHERE t.parent_name=%s
# 		GROUP BY t.name
# 	""", frappe.session.user, as_dict=True)
# 	return messages

