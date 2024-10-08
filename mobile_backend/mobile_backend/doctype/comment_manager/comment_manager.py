# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CommentManager(Document):
	@frappe.whitelist()
	def get_comments(self, document, status):
		filters = {
			"parenttype": document,
		}
		if status != 'All':
			filters["status"] = status
		comments = frappe.db.get_list('Mobile Comment', fields=["name","comment", "user", "status"], filters=filters)
		self.comments = []
		for comment in comments:
			tbl_comment = self.append("comments")
			tbl_comment.comment = comment["comment"]
			tbl_comment.user = comment["user"]
			tbl_comment.status = comment["status"]
			tbl_comment.name = comment["name"]
		return {"msg": "done"}
	@frappe.whitelist()
	def set_status(self, comments, new_status, document):
		for comment in comments:
			try:
				frappe.db.set_value("Mobile Comment", comment, {"status":new_status})
			except:
				continue
		for doc_name in frappe.db.get_list(document):
			try:
				doc = frappe.get_doc(document, doc_name.name)
				doc.save()
				doc.submit()
			except:
				continue

		return {"msg": "done"}