# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.password import update_password
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
		parents = tree.findall('Parent')
		#self.enqueue_add_parents(parents, password)
		add_parents(parents, password)

	def import_student_data(self, url):
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		students = tree.findall('Student')
		add_students(students)

def add_user(user, fullname):
	try:
		frappe.db.sql("""
		INSERT INTO 
		`tabUser`(name, creation, modified, modified_by, owner, 
		username, full_name, first_name,email, user_type) 
		VALUES("{user}", now(), now(), 'Administrator', 'Administrator',
				"{user}", "{name}", "{name}", "{user}", "Website User")
		ON DUPLICATE key UPDATE `full_name`="{name}"
		""".format(user= user, name= fullname))
		frappe.db.commit()
		return True
	except:
		return False

def add_parent(year, branch, contract, name, mobile):
	try:
		frappe.db.sql("""
						INSERT INTO `tabSchool Parent`(name, creation, modified, modified_by, owner, 
							year, branch, contract_no, parent_name, mobile_no)
						VALUES("{mobile}", now(), now(),  'Administrator', 'Administrator',
						"{year}", "{branch}", "{contract}", "{name}", "{mobile}")
						ON DUPLICATE key UPDATE `year`="{year}", `branch`="{branch}", 
						`contract_no`="{contract}", `parent_name`="{name}", `mobile_no`="{mobile}"
						""".format(year=year, branch=branch, contract=contract, name=name, mobile=mobile))
		frappe.db.commit()
		return True
	except:
		return False

def add_parents(parents, password):
	for parent in parents:
		try:
			year_code = parent.find('YEARCODE').text
			branch_code = parent.find('BRNCODE').text
			contract_no = parent.find('CONNO').text
			parent_name = parent.find('CONNAME').text
			mobile_no = parent.find('MOBILENO').text

			if (mobile_no and len(mobile_no) > 7) and (parent_name and len(parent_name) > 1):
				try:
					#if not frappe.db.exists({"doctype": "User", "name": mobile_no}):
						# user = frappe.get_doc({
						# 	"doctype": "User",
						# 	"first_name": parent_name,
						# 	"email": mobile_no + "@mail.com",
						# 	"mobile_no": mobile_no,
						# 	"send_welcome_email": 0
						# }).insert()
						# user.new_password = password
						# user.save()
					if add_user(mobile_no, parent_name):
						update_password(user=mobile_no, pwd=password)
				except:
					pass
				try:
					#if not frappe.db.exists({"doctype": "School Parent", "name": mobile_no}):
						# frappe.get_doc({
						# "doctype": "School Parent",
						# "year": year_code,
						# "branch": branch_code,
						# "contract_no":contract_no,
						# "parent_name": parent_name,
						# "mobile_no": mobile_no
						# }).insert()
					add_parent(year_code, branch_code, contract_no, parent_name, mobile_no)
				except:
					pass
		except:
			pass
	frappe.db.commit()

def add_students(students):
	for student in students:
		try:
			year_code = student.find('YEARCODE').text
			branch_code = student.find('BRNCODE').text
			contract_no = student.find('CONNO').text
			mobile_no = student.find('MOBILENO').text
			student_no = student.find('STDNO').text
			student_name = student.find('STDNAME').text
			class_code = student.find('CLSCODE').text
			section_code = student.find('SECCODE').text
			student_gender = student.find('STDGENDER').text
			if frappe.db.exists({"doctype": "School Parent", "name": mobile_no}):
				name = year_code + '-' + branch_code + '-' + contract_no + '-' + student_no
				section = class_code + '-' + section_code
				frappe.db.sql("""
						INSERT INTO `tabSchool Student`(name, creation, modified, modified_by, owner, 
							year, branch, contract_no, parent_no, student_no, student_name, student_gender, class, section)
						VALUES("{name}", now(), now(),  'Administrator', 'Administrator',
						"{year}", "{branch}", "{contract}", "{mobile}", "{student_no}", "{student_name}",
							"{student_gender}", "{class_code}", "{section}")
						ON DUPLICATE key UPDATE `year`="{year}", `branch`="{branch}", 
						`contract_no`="{contract}", `parent_no`="{mobile}", `student_no`="{student_no}",
						`student_name`="{student_name}", `student_gender`="{student_gender}", `class`="class_code", `section`="{section}"
						""".format(year=year_code, branch=branch_code, contract=contract_no, name=name, mobile=mobile_no,
							student_no=student_no,student_name=student_name,student_gender=student_gender,
							class_code=class_code,section=section
						))
				frappe.db.commit()
		except:
			pass