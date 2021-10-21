# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import utils

class Announcement(Document):
	def before_save(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)


@frappe.whitelist(allow_guest=True)
def get_announcements():
	# return frappe.db.get_all('Announcement',
	# # filters={
    # # 'creation': ['>', '2019-09-08']
	# # },
    # fields=['name','title', 'description', 'creation', 'likes', 'views'],
	# # order_by='creation desc',
	# # start=0,
    # # page_length=20,
	# )
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	# return frappe.db.sql("""
	# 	SELECT name, title, description, creation, likes, views, approved_comments from `tabAnnouncement`
	# """, as_dict=True)
	return frappe.db.sql("""
		SELECT ta.name, ta.title, ta.description, ta.creation, ta.likes, ta.views, ta.approved_comments, 
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabAnnouncement` as ta
		LEFT JOIN `tabMobile Like` as tl ON (ta.name<=>tl.parent AND tl.parenttype='Announcement' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (ta.name<=>tv.parent AND tv.parenttype='Announcement' AND tv.user=%s)
	""", (user, user) ,as_dict=True)

@frappe.whitelist(allow_guest=True)
def view_announcement():
	announcement = frappe.form_dict.announcement
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Announcement", announcement)
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
	announcement = frappe.form_dict.announcement
	comment = frappe.form_dict.comment
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Announcement", announcement)
	if doc:
		rec = doc.append("comments")
		rec.comment = comment
		rec.user = user
		rec.status = 'Pending'
		doc.save(ignore_permissions=True)
		return rec.name

@frappe.whitelist(allow_guest=True)
def get_comments():
	announcement = frappe.form_dict.announcement
	return frappe.db.sql("""
		SELECT name, comment FROM `tabMobile Comment` WHERE parent=%s AND parenttype='Announcement' AND status='Approved'
	""",announcement, as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='Announcement'
	""",comment_name)
	frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def like_announcement():
	announcement = frappe.form_dict.announcement
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Announcement", announcement)
	if doc:
		try:
			rec = doc.append('likes_table')
			rec.user = user
			doc.save(ignore_permissions=True)
			frappe.db.commit()
		except:
			return

	
@frappe.whitelist(allow_guest=True)
def dislike_announcement():
	announcement = frappe.form_dict.announcement
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.db.sql("""
		DELETE FROM `tabMobile Like` WHERE parent=%s AND parenttype='Announcement' AND user=%s
	""", (announcement, user))
	frappe.get_doc("Announcement", announcement).save(ignore_permissions=True)
	frappe.db.commit()
	
