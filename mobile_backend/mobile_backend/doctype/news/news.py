# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import notification, utils

class News(Document):
	def after_insert(self):
		notification.send_topic_notification('news', 'New news', self.title)
	def before_save(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)



@frappe.whitelist(allow_guest=True)
def get_news():
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT 'News' as type, tn.name, tn.title, tn.description, tn.creation, tn.likes, tn.views, tn.approved_comments,
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked  FROM `tabNews` AS tn
		LEFT JOIN `tabMobile Like` as tl ON (tn.name<=>tl.parent AND tl.parenttype='News' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (tn.name<=>tv.parent AND tv.parenttype='News' AND tv.user=%s)
	""",(user, user), as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_single_news():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT 'News' as type, tn.name, tn.title, tn.description, tn.creation, tn.likes, tn.views, tn.approved_comments,
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked  FROM `tabNews` AS tn
		LEFT JOIN `tabMobile Like` as tl ON (tn.name<=>tl.parent AND tl.parenttype='News' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (tn.name<=>tv.parent AND tv.parenttype='News' AND tv.user=%s)
		WHERE tn.name=%s
	""",(user, user, news), as_dict=True)

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
	user_name = frappe.db.get_value("User", frappe.session.user, ["full_name"])
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("News", news)
	if doc:
		rec = doc.append("comments")
		rec.comment = comment
		rec.user = user
		rec.user_name = user_name
		rec.status = 'Pending'
		doc.save(ignore_permissions=True)
		return rec.name

@frappe.whitelist(allow_guest=True)
def get_comments():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT user_name, name, comment, user=%s as is_owned FROM `tabMobile Comment` WHERE parent=%s AND parenttype='News' AND status='Approved'
	""",(user, news), as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user) 
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='News' AND user=%s
	""",(comment_name, user))
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
	