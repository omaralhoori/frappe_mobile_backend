# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SchoolBranch(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_branches():
	return frappe.db.sql("""SELECT name, branch_name FROM `tabSchool Branch`""", as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_classes():
	return frappe.db.sql("""SELECT name, class_name FROM `tabSchool Class`""", as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_sections():
	return frappe.db.sql("""SELECT name, section_name FROM `tabSchool Section`""", as_dict=True)