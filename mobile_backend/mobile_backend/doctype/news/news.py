# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import utils

class News(Document):
	def before_save(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)



@frappe.whitelist(allow_guest=True)
def get_news():
	return frappe.db.sql("""
		SELECT name, title, description, creation, likes, views, approved_comments from `tabNews`
	""", as_dict=True)

@frappe.whitelist(allow_guest=True)
def view_news():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("News", news)
	if doc:
		try:
			rec = doc.append('views_table')
			rec.user = user
			doc.save(ignore_permissions=True)
			frappe.db.commit()
		except:
			return


@frappe.whitelist(allow_guest=True)
def add_comment():
	news = frappe.form_dict.news
	comment = frappe.form_dict.comment
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("News", news)
	if doc:
		rec = doc.append("comments")
		rec.comment = comment
		rec.user = user
		rec.status = 'Pending'
		doc.save(ignore_permissions=True)
		return rec.name

@frappe.whitelist(allow_guest=True)
def get_comments():
	news = frappe.form_dict.news
	return frappe.db.sql("""
		SELECT name, comment FROM `tabMobile Comment` WHERE parent=%s AND parenttype='News' AND status='Approved'
	""",news, as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='News'
	""",comment_name)
	frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def like_news():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("News", news)
	if doc:
		try:
			rec = doc.append('likes_table')
			rec.user = user
			doc.save(ignore_permissions=True)
			frappe.db.commit()
		except:
			return

	
@frappe.whitelist(allow_guest=True)
def dislike_news():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.db.sql("""
		DELETE FROM `tabMobile Like` WHERE parent=%s AND parenttype='News' AND user=%s
	""", (news, user))
	frappe.get_doc("News", news).save(ignore_permissions=True)
	frappe.db.commit()
	