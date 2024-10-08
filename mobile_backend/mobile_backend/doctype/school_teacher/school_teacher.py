# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import hashlib

class SchoolTeacher(Document):
	def validate(self):
		pass
		# if self.password == len(self.password) * "*":
		# 	pass
		# else:
		# 	#update_password(self)
		# 	self.password = hash_password(self.password)

@frappe.whitelist()
def update_teacher_password(pwd):
	user = frappe.session.user
	doc = frappe.get_doc("School Teacher", user)
	if doc:
		if pwd and len(pwd) > 0:
			hashPwd = hash_password(pwd)
			doc.password = hashPwd
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	else:
		frappe.local.response['http_status_code'] = 404
		return {}
def hash_password(pwd):
# 	passlibctx = CryptContext(
# 	schemes=[
# 		"pbkdf2_sha256",
# 		# "argon2",
# 		# "frappe_legacy",
# 	],
# 	# deprecated=[
# 	# 	"frappe_legacy",
# 	# ],
# )
	encoded = pwd.encode()
	result = hashlib.sha256(encoded)
	
	return result.hexdigest()

@frappe.whitelist()
def login_teacher(pwd):
	user = frappe.session.user
	hashPwd = hash_password(pwd)
	password = frappe.db.get_value("School Teacher", user, ["password"])
	if password:
		if hashPwd == password:
			frappe.local.response['http_status_code'] = 200
		else:
			frappe.local.response['http_status_code'] = 401
	else:
		frappe.local.response['http_status_code'] = 404
	return