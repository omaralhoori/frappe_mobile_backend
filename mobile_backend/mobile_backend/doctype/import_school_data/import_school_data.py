# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests
from xml.etree import ElementTree

class ImportSchoolData(Document):
	def import_branch_data(self, url):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for branch in tree.findall('Branch'):
			try:
				code = branch.find('CS_BRN_CODE').text
				name = branch.find('CS_BRN_ADESC').text
				tel = branch.find('CS_BRN_TEL').text
				fax = branch.find('CS_BRN_FAX').text
				address = branch.find('CS_BRN_ADD').text
				frappe.get_doc({
					"doctype": "School Branch",
					"branch_code": code,
					"branch_name": name,
					"telephone": tel,
					"fax": fax,
					"address": address
				}).insert()
			except:
				pass
		return {}

	def import_year_data(self, url):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for year in tree.findall('Year'):
			try:
				code = year.find('YEARCODE').text
				name = year.find('YEARNAME').text
				frappe.get_doc({
					"doctype": "School Year",
					"year_code": code,
					"year_name": name
				}).insert()
			except:
				pass
		return {}

	def import_class_data(self, url):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for _class in tree.findall('Class'):
			try:
				code = _class.find('CLSCODE').text
				name = _class.find('CLSNAME').text
				frappe.get_doc({
					"doctype": "School Class",
					"class_code": code,
					"class_name": name
				}).insert()
			except:
				pass
		return {}

	def import_section_data(self, url):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for _class in tree.findall('Class'):
			try:
				class_code = _class.find('CLSCODE').text
				sections = _class.findall('Section')
				for section in sections:
					try:
						code = section.find('SECCODE').text
						name = section.find('SECNAME').text
						frappe.get_doc({
							"doctype": "School Section",
							"class": class_code,
							"section_code": code,
							"section_name": name
						}).insert()
					except:
						pass
			except:
				pass
		return {}

	def import_parent_data(self, url, password):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		#parents = tree.findall('Parent')
		for parent in tree.findall('Parent'):
			try:
				year_code = parent.find('YEARCODE').text
				branch_code = parent.find('BRNCODE').text
				contract_no = parent.find('CONNO').text
				parent_name = parent.find('CONNAME').text
				mobile_no = parent.find('MOBILENO').text
				try:
					user = frappe.get_doc({
						"doctype": "User",
						"first_name": parent_name,
						"email": mobile_no + "@mail.com",
						"mobile_no": mobile_no,
						"send_welcome_email": 0
					}).insert()
					user.new_password = password
					user.save()
				except:
					pass
				# frappe.db.sql("""
				
				# """)
				# try:
				# 	frappe.get_doc({
				# 		"doctype": "School Parent",
				# 		"year": year_code,
				# 		"branch": branch_code,
				# 		"contract_no":contract_no,
				# 		"parent_name": parent_name,
				# 		"mobile_no": mobile_no
				# 	}).insert()
				# except:
				# 	pass
			except:
				pass
		return {}
