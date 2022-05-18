# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import notification, utils

class News(Document):
	# def after_insert(self):
	# 	print("After inserted")

	def on_submit(self):
		self.send_notification()

	def send_notification(self):
		settings = frappe.get_doc("School Settings")
		if settings.news_notifiction == 1:
			title = settings.news_title if settings.news_title else "New News"
			notification.send_topic_notification('news', title, self.title, {
				"type": "News",
				"name": self.name
			})
			
	def on_update_after_submit(self):
		old_doc = self.get_doc_before_save()
		if old_doc:
			if old_doc.title != self.title or old_doc.description != self.description:
				self.send_notification()

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
			doc.submit()
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
		doc.submit()
		return rec.name

@frappe.whitelist(allow_guest=True)
def get_comments():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT IF(tu.full_name IS NULL, "Guest", tu.full_name) as user_name,tu.user_image, tmc.name, tmc.comment, tmc.user=%s as is_owned
		FROM `tabMobile Comment` AS tmc
		LEFT JOIN `tabUser` AS tu ON tmc.user=tu.name
		WHERE tmc.parent=%s AND tmc.parenttype='News' AND tmc.status='Approved'
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
			doc.submit()
			frappe.db.commit()
		except:
			return

	
@frappe.whitelist(allow_guest=True)
def dislike_news():
	news = frappe.form_dict.news
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	frappe.db.sql("""
		DELETE FROM `tabMobile Like` WHERE parent=%s AND parenttype='News' AND user=%s
	""", (news, user))
	doc = frappe.get_doc("News", news)
	doc.save(ignore_permissions=True)
	doc.submit()
	frappe.db.commit()
	