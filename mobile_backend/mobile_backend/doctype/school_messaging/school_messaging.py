# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from email import message
from mobile_backend.mobile_backend.notification import send_multiple_notification

from mobile_backend.mobile_backend.utils import get_current_site_name
import frappe
from frappe.model.document import Document
from frappe.utils.dateutils import datetime
import threading
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
		ORDER BY sending_date
		""", (self.name), as_dict=True)
		return messages


@frappe.whitelist()
def get_messages():
	messages = frappe.db.sql("""
		SELECT tsm.name, tsm.title, tsm.creation, tsm.message_type, tsm.message_name, tsm.student_no, tsm.student_name, tsm.thumbnail, 
		GROUP_CONCAT(tf.file_url SEPARATOR  ";") as attachments
		FROM `tabSchool Messaging` as tsm
		LEFT JOIN `tabFile` AS tf on tsm.name=tf.attached_to_name AND attached_to_doctype='School Messaging'
		WHERE parent_name=%s
		GROUP BY tsm.name
		ORDER BY creation DESC
	""", frappe.session.user, as_dict=True)
	for message in messages:
		doc = frappe.get_doc("School Messaging", message["name"])
		message["messages"] = doc.get_messages() if doc else []
	return messages

@frappe.whitelist()
def get_message():
	message_name = frappe.form_dict.message_name
	message_type = frappe.form_dict.message_type
	message = frappe.db.sql("""
		SELECT name, title, creation, message_type, message_name, student_no, student_name
		FROM `tabSchool Messaging`
		WHERE parent_name=%s AND message_name=%s AND message_type=%s
		LIMIT 1;
	""", (frappe.session.user, message_name, message_type), as_dict=True)
	#for message in messages:
	if len(message) > 0:
		message = message[0]
	else:
		frappe.local.response['http_status_code'] = 404
		return
	doc = frappe.get_doc("School Messaging", message["name"])
	message["messages"] = doc.get_messages() if doc else []
	return message


@frappe.whitelist()
def get_unread_messages():
	user = frappe.session.user
	return frappe.db.sql("""
	SELECT COUNT(m2.parent_name) as unread_messages, m2.message_type FROM `tabSchool Messages` as m1
		INNER JOIN `tabSchool Messaging`as m2 ON m1.parent=m2.name
		WHERE m1.is_administration=1 AND m1.is_read=0 AND m2.parent_name=%s
		GROUP BY m2.message_type, m2.parent_name;
	""", user, as_dict=True)

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
		doc.seen_by_parent = "Seen"
		doc.save(ignore_permissions=True)
		frappe.db.commit()

@frappe.whitelist()
def send_parent_message():
	title = frappe.form_dict.title
	message = frappe.form_dict.message
	branch = frappe.form_dict.branch
	doc = frappe.get_doc({
					"doctype": "School Messaging",
					"parent_name": frappe.session.user,
					"title": title,
					"branch": branch,
					"message_type": "School Direct Message",
					"status": 'Not seen',
					"seen_by_parent": 'Seen',
				})
	row = doc.append("messages")
	row.sender_name = frappe.db.get_value("User", frappe.session.user, "full_name")
	row.message = message
	row.is_administration = 0
	row.sending_date = datetime.datetime.now()

	doc.save(ignore_permissions=True)

def update_attachment_file(old_dt, old_dn, new_dn, new_dt):
	frappe.db.sql(f"""
		UPDATE `tabFile` SET attached_to_name="{new_dn}" , attached_to_doctype="{new_dt}"
		WHERE attached_to_name="{old_dn}" AND attached_to_doctype="{old_dt}"
	""")
def add_attachment_file(old_dt, old_dn, new_dn, new_dt):
	frappe.db.sql(f"""
		INSERT INTO tabFile( name,creation, modified, modified_by, owner, file_name, file_url, 
		attached_to_name, file_size, attached_to_doctype, is_private,
		is_home_folder, folder, attached_to_field, content_hash ) select CONCAT(name,"-{new_dn}"),creation, modified, modified_by, owner, file_name, file_url, 
		"{new_dn}", file_size, "{new_dt}", is_private,
		is_home_folder, folder, attached_to_field, content_hash from tabFile where attached_to_name="{old_dn}" AND attached_to_doctype="{old_dt}";
	""")

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

def add_messages(messages, message_type, message_title):
	kwargs = {
			"messages":messages,"message_type":message_type, "message_title":message_title, 
		}
	print(messages)
	print(len(messages))
	if len(messages) > 25:
		kwargs["site_name"] = get_current_site_name()
		thread = threading.Thread(target=send_messages_async, kwargs=kwargs)
		thread.start()
		return 2
	else:
		send_messages_async(**kwargs)
		return 1

def send_messages_async(messages, message_type, message_title, site_name=None):
	if site_name:
		frappe.init(site=site_name)
		frappe.connect()
	for message in messages:
		create_message(message_type, message_title, message)

	frappe.db.commit()

def create_message(message_type, message_title, message):
	if message_type == "School Group Message":
		branch_no, contract_no, student_no, msg = message.get("branch_code"), message.get("contract_no"), message.get("student_no"), message.get("message")
		print(branch_no, contract_no, student_no, msg)
		if not branch_no or not contract_no or not student_no or not msg: return
		add_student_message(branch_no, contract_no, student_no, message_title, msg)
	else:
		branch_no, contract_no, msg = message.get("branch_code"), message.get("contract_no"), message.get("message")
		if not branch_no or not contract_no or not msg: return
		add_parent_message(branch_no, contract_no, message_title, msg)

def add_student_message(branch_no, contract_no, student_no, message_title, msg):
	parent = frappe.db.get_value("School Parent", {"contract_no": contract_no, "branch": branch_no}, ["name","parent_name", "device_token"])
	if not parent: return
	parent_id, parent_name, device_token = parent
	student = frappe.db.get_value("School Student", {"parent_no": parent_id, "branch": branch_no, "contract_no": contract_no, "student_no": student_no}, ["student_name"])
	if not student: return
	student_name = student
	doc = frappe.get_doc({
		"doctype": "School Messaging",
		"parent_name": parent_id,
		"student_no": student_no,
		"student_name": student_name,
		"title": message_title,
		"branch": branch_no,
		"message_type": "School Group Message",
	})
	row = doc.append("messages")
	row.sender_name = "Administration"
	row.message = msg
	row.is_administration = 1
	row.sending_date = datetime.datetime.now()
	doc.insert()
	try:
		send_multiple_notification(device_token, message_title, msg, {
			"type": "School Group Message",
			"student_no": student_no,
			"name": doc.name
		})
	except BaseException as e:
		print(f"Unexpected {e=}, {type(e)=}")


def add_parent_message(branch_no, contract_no, message_title, msg):
	parent = frappe.db.get_value("School Parent", {"contract_no": contract_no, "branch": branch_no}, ["name","parent_name","device_token"])
	if not parent: return
	parent_id, parent_name, device_token = parent
	doc = frappe.get_doc({
		"doctype": "School Messaging",
		"parent_name": parent_id,
		"title": message_title,
		"branch": branch_no,
		"message_type": "School Direct Message",
	})
	row = doc.append("messages")
	row.sender_name = "Administration"
	row.message = msg
	row.is_administration = 1
	row.sending_date = datetime.datetime.now()
	doc.insert()
	try:
		send_multiple_notification(device_token, message_title, msg, {
			"type": "School Direct Message",
			"name": doc.name
		})
	except BaseException as e:
		print(f"Unexpected")
	
