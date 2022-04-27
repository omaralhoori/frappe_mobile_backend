# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import utils

class GalleryAlbum(Document):
	def on_update_after_submit(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)


@frappe.whitelist(allow_guest=True)
def get_albums():
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT a.name, a.branch, a.class_code, a.section ,a.title, a.description, a.creation, a.likes, a.views, a.approved_comments, ftable.file_url ,IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabGallery Album` as a
		LEFT JOIN `tabMobile Like` as tl ON (a.name<=>tl.parent AND tl.parenttype='Gallery Album' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (a.name<=>tv.parent AND tv.parenttype='Gallery Album' AND tv.user=%s)
		INNER JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Gallery Album'
		GROUP BY f.attached_to_name) AS ftable 
		ON a.name=ftable.attached_to_name
		WHERE a.docstatus=1
	""", (user, user),as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_album():
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT a.name, a.branch, a.class_code, a.section, a.title, a.description, a.creation, a.likes, a.views, a.approved_comments, ftable.file_url ,IF(tv.user IS NULL,0,1) AS is_viewed,  IF(tl.user IS NULL,0,1) AS is_liked from `tabGallery Album` as a
		LEFT JOIN `tabMobile Like` as tl ON (a.name<=>tl.parent AND tl.parenttype='Gallery Album' AND tl.user=%s)
		LEFT JOIN `tabMobile View` as tv ON (a.name<=>tv.parent AND tv.parenttype='Gallery Album' AND tv.user=%s)
		INNER JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Gallery Album'
		GROUP BY f.attached_to_name) AS ftable 
		ON a.name=ftable.attached_to_name
		WHERE a.name=%s
	""", (user, user, album),as_dict=True)


@frappe.whitelist(allow_guest=True)
def view_album():
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Gallery Album", album)
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
	album = frappe.form_dict.album
	comment = frappe.form_dict.comment
	user_name = frappe.db.get_value("User", frappe.session.user, ["full_name"])
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Gallery Album", album)
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
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	return frappe.db.sql("""
		SELECT IF(tu.full_name IS NULL, "Guest", tu.full_name) as user_name,tu.user_image, tmc.name, tmc.comment, tmc.user=%s as is_owned
		FROM `tabMobile Comment` AS tmc
		LEFT JOIN `tabUser` AS tu ON tmc.user=tu.name
		WHERE tmc.parent=%s AND tmc.parenttype='Gallery Album' AND tmc.status='Approved'
	""",(user, album), as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user) 
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='Gallery Album' AND user=%s
	""",(comment_name, user))
	frappe.db.commit()


@frappe.whitelist(allow_guest=True)
def like_album():
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Gallery Album", album)
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
def dislike_album():
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	frappe.db.sql("""
		DELETE FROM `tabMobile Like` WHERE parent=%s AND parenttype='Gallery Album' AND user=%s
	""", (album, user))
	doc = frappe.get_doc("Gallery Album", album)
	doc.save(ignore_permissions=True)
	doc.submit()
	frappe.db.commit()
	
