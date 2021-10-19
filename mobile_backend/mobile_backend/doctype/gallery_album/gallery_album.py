# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from mobile_backend.mobile_backend import utils

class GalleryAlbum(Document):
	def before_save(self):
		approved_comments = 0
		for comment in self.comments:
			if comment.status == 'Approved': approved_comments += 1
		self.approved_comments = approved_comments
		self.likes = len(self.likes_table)
		self.views = len(self.views_table)


@frappe.whitelist(allow_guest=True)
def get_albums():
	return frappe.db.sql("""
		SELECT a.name, a.title, a.description, a.creation, a.likes, a.views, a.approved_comments, ftable.file_url from `tabGallery Album` as a
		INNER JOIN
		(SELECT f.attached_to_name ,GROUP_CONCAT(f.file_url) as file_url FROM `tabFile` AS f
		WHERE f.attached_to_doctype='Gallery Album'
		GROUP BY f.attached_to_name) AS ftable 
		ON a.name=ftable.attached_to_name
	""", as_dict=True)


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
			frappe.db.commit()
		except:
			return

@frappe.whitelist(allow_guest=True)
def add_comment():
	album = frappe.form_dict.album
	comment = frappe.form_dict.comment
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.get_doc("Gallery Album", album)
	if doc:
		rec = doc.append("comments")
		rec.comment = comment
		rec.user = user
		rec.status = 'Pending'
		doc.save(ignore_permissions=True)
		return rec.name

@frappe.whitelist(allow_guest=True)
def get_comments():
	album = frappe.form_dict.album
	return frappe.db.sql("""
		SELECT name, comment FROM `tabMobile Comment` WHERE parent=%s AND parenttype='Gallery Album' AND status='Approved'
	""",album, as_dict=True)

@frappe.whitelist(allow_guest=True)
def remove_comment():
	comment_name = frappe.form_dict.comment_name
	frappe.db.sql("""
		DELETE FROM `tabMobile Comment` WHERE name=%s AND parenttype='Gallery Album'
	""",comment_name)
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
			frappe.db.commit()
		except:
			return

	
@frappe.whitelist(allow_guest=True)
def dislike_album():
	album = frappe.form_dict.album
	user = frappe.form_dict.user
	user = utils.get_or_create_user(user)
	doc = frappe.db.sql("""
		DELETE FROM `tabMobile Like` WHERE parent=%s AND parenttype='Gallery Album' AND user=%s
	""", (album, user))
	frappe.get_doc("Gallery Album", album).save(ignore_permissions=True)
	frappe.db.commit()
	
