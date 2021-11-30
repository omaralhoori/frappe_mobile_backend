# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import utils
from mobile_backend.mobile_backend import notification

class Announcement(Document):
	def after_insert(self):
		data = {
			"type": "Announcement",
			"name": self.name
		}
		notification.send_topic_notification('announcement', 'New announcement', self.title,data )
	def before_save(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)

	# def validate(self):
	# 	if self.get("__islocal") or not self.get("name"):
	# 		pass
	# 	else: print("Old ann")
		
	# def save(self, *args, **kwargs):
	# 	if self.get("__islocal") or not self.get("name"):
	# 		print("New ann")
	# 	else: print("Old ann")
	# 	print("savesss")
	# 	return self._save(*args, **kwargs)

@frappe.whitelist(allow_guest=True)
def get_all_contents():
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	skip = frappe.form_dict.skip
	limit = frappe.form_dict.limit
	LIMIT = ""
	if skip is not None and limit is not None:
		LIMIT = "LIMIT {},{}".format(skip, limit)
	return frappe.db.sql("""
	SELECT type, name, title, description, creation, likes, views, approved_comments, is_viewed, is_liked, file_url FROM
		(SELECT 'Announcement' as type, ta.name, ta.title, ta.description, ta.creation, ta.likes, ta.views, ta.approved_comments, ftable.file_url,
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabAnnouncement` as ta
		LEFT JOIN `tabMobile Like` as tl ON (ta.name<=>tl.parent AND tl.parenttype='Announcement' AND tl.user="{user}")
		LEFT JOIN `tabMobile View` as tv ON (ta.name<=>tv.parent AND tv.parenttype='Announcement' AND tv.user="{user}")
		LEFT JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Announcement'
		GROUP BY f.attached_to_name) AS ftable 
		ON ta.name=ftable.attached_to_name
		UNION
		SELECT 'News' as type, tn.name, tn.title, tn.description, tn.creation, tn.likes, tn.views, tn.approved_comments,ftable.file_url,
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked  FROM `tabNews` AS tn
		LEFT JOIN `tabMobile Like` as tl ON (tn.name<=>tl.parent AND tl.parenttype='News' AND tl.user="{user}")
		LEFT JOIN `tabMobile View` as tv ON (tn.name<=>tv.parent AND tv.parenttype='News' AND tv.user="{user}")
		LEFT JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='News'
		GROUP BY f.attached_to_name) AS ftable 
		ON tn.name=ftable.attached_to_name
		) as all_content
		ORDER BY creation DESC
		{limit}
	""".format(user=user, limit=LIMIT) ,as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_contents_version():
	return frappe.db.sql("""
	SELECT type, name, version FROM
		(SELECT 'Announcement' as type, ta.name, ta.version FROM `tabAnnouncement` AS ta
		UNION
		SELECT 'News' as type, tn.name, tn.version FROM `tabNews` AS tn
		) as all_content;
	""", as_dict=True)

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
	return frappe.db.sql("""
		SELECT 'Announcement' as type, ta.name, ta.title, ta.description, ta.creation, ta.likes, ta.views, ta.approved_comments, ftable.file_url , 
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabAnnouncement` as ta
		LEFT JOIN `tabMobile Like` as tl ON (ta.name<=>tl.parent AND tl.parenttype='Announcement' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (ta.name<=>tv.parent AND tv.parenttype='Announcement' AND tv.user=%s)
		LEFT JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Announcement'
		GROUP BY f.attached_to_name) AS ftable 
		ON ta.name=ftable.attached_to_name
	""", (user, user) ,as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_announcement():
	announcement = frappe.form_dict.announcement
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT 'Announcement' as type, ta.name, ta.title, ta.description, ta.creation, ta.likes, ta.views, ta.approved_comments, ftable.file_url , 
		IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabAnnouncement` as ta
		LEFT JOIN `tabMobile Like` as tl ON (ta.name<=>tl.parent AND tl.parenttype='Announcement' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (ta.name<=>tv.parent AND tv.parenttype='Announcement' AND tv.user=%s)
		LEFT JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Announcement'
		GROUP BY f.attached_to_name) AS ftable 
		ON ta.name=ftable.attached_to_name
		WHERE ta.name=%s
	""", (user, user, announcement) ,as_dict=True)

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
	user_name = frappe.db.get_value("User", frappe.session.user, ["full_name"])
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Announcement", announcement)
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
	announcement = frappe.form_dict.announcement
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT IF(tu.full_name IS NULL, "Guest", tu.full_name) as user_name,tu.user_image, tmc.name, tmc.comment, tmc.user=%s as is_owned
		FROM `tabMobile Comment` AS tmc
		LEFT JOIN `tabUser` AS tu ON tmc.user=tu.name
		WHERE tmc.parent=%s AND tmc.parenttype='Announcement' AND tmc.status='Approved'
	""",(user, announcement), as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user) 
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='Announcement' AND user=%s
	""",(comment_name, user))
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
	
