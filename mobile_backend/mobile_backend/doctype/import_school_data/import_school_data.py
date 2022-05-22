# -*- coding: utf-8 -*-
# Copyright (c) 2021, Omar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.password import update_password
import requests
from xml.etree import ElementTree

class ImportSchoolData(Document):
	@frappe.whitelist()
	def import_branch_data(self):
		rel_link = '/reports/rwservlet?report=STRMOBBRN'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id
				}
				url = '{data_url}{rel_link}&userid={user_id}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for branch in tree.findall('Branch'):
			try:
				code = branch.find('CS_BRN_CODE').text
				name = branch.find('CS_BRN_ADESC').text
				tel = branch.find('CS_BRN_TEL').text
				fax = branch.find('CS_BRN_FAX').text
				address = branch.find('CS_BRN_ADD').text
				#code = branch.find('BRNCODE').text
				#name = branch.find('BRNNAME').text
				#tel = branch.find('BRNTEL').text
				#fax = branch.find('BRNFAX').text
				#address = branch.find('BRNADD').text
				if not frappe.db.exists('School Branch', code):
					frappe.get_doc({
						"doctype": "School Branch",
						"branch_code": code,
						"branch_name": name,
						"telephone": tel,
						"fax": fax,
						"address": address
					}).insert()
				else:
					frappe.db.set_value("School Branch", code, {
						"branch_code": code,
						"branch_name": name,
						"telephone": tel,
						"fax": fax,
						"address": address
					})
			except:
				pass
		return {}
	@frappe.whitelist()
	def import_year_data(self):
		rel_link = '/reports/rwservlet?report=STRMOBYER'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id
				}
				url = '{data_url}{rel_link}&userid={user_id}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for year in tree.findall('Year'):
			try:
				code = year.find('YEARCODE').text
				name = year.find('YEARNAME').text
				if not frappe.db.exists('School Year', code):
					frappe.get_doc({
						"doctype": "School Year",
						"year_code": code,
						"year_name": name
					}).insert()
				else:
					frappe.db.set_value("School Year", code, {
						"year_code": code,
						"year_name": name,
					})
			except:
				pass
		return {}
	@frappe.whitelist()
	def import_class_data(self):
		rel_link = '/reports/rwservlet?report=STRMOBCLS'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id
				}
				url = '{data_url}{rel_link}&userid={user_id}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return
		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		for _class in tree.findall('Class'):
			try:
				code = _class.find('CLSCODE').text
				name = _class.find('CLSNAME').text
				if not frappe.db.exists('School Class', code):
					frappe.get_doc({
						"doctype": "School Class",
						"class_code": code,
						"class_name": name
					}).insert()
				else:
					frappe.db.set_value("School Class", code, {
						"class_code": code,
						"class_name": name,
					})
			except:
				pass
		return {}
	@frappe.whitelist()
	def import_section_data(self):
		rel_link = '/reports/rwservlet?report=STRMOBSEC'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id
				}
				url = '{data_url}{rel_link}&userid={user_id}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return
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
						if not frappe.db.exists('School Section',class_code +'-'+code):
							frappe.get_doc({
								"doctype": "School Section",
								"class": class_code,
								"section_code": code,
								"section_name": name
							}).insert()
						else:
							frappe.db.set_value("School Section", class_code +'-'+code, {
									"class": class_code,
									"section_code": code,
									"section_name": name
								})
					except:
						pass
			except:
				pass
		return {}
	@frappe.whitelist()
	def import_parent_data(self, branch, year, password):
		rel_link = '/reports/rwservlet?report=STRMOBCON'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id,
					"branch": branch,
					"year": year
				}
				url = '{data_url}{rel_link}&userid={user_id}&PBRN={branch}&PYEAR={year}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return

		res = requests.get(url)
		tree = ElementTree.fromstring(res.content)
		parents = tree.findall('Parent')
		#self.enqueue_add_parents(parents, password)
		add_parents(parents, password)
	@frappe.whitelist()
	def import_student_data(self, branch, year):
		rel_link = '/reports/rwservlet?report=STRMOBSTD'
		data_settings = frappe.get_doc("School Settings")
		url=None
		if data_settings.data_url and data_settings.data_url != '':
			if data_settings.user_id and data_settings.user_id != '':
				kwargs = {
					"data_url": data_settings.data_url,
					"rel_link":rel_link,
					"user_id": data_settings.user_id,
					"branch": branch,
					"year": year
				}
				url = '{data_url}{rel_link}&userid={user_id}&PBRN={branch}&PYEAR={year}'.format(**kwargs)
		if not url:
			frappe.throw(_("Data url is not correct"))
			return
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
				if not frappe.db.exists('School Parent',mobile_no):
					try:
						if add_user(mobile_no, parent_name):
							update_password(user=mobile_no, pwd=password)
					except:
						pass
					try:
						add_parent(year_code, branch_code, contract_no, parent_name, mobile_no)
					except:
						pass
				else:
					try:
						update_parent(year_code, branch_code, contract_no, parent_name, mobile_no)
					except:
						print("Error")
		except:
			pass
	frappe.db.commit()

def update_parent(year, branch, contract, name, mobile):
	frappe.db.sql("""
						UPDATE `tabSchool Parent`
						SET
							modified=now(), 
							year="{year}", 
							branch="{branch}", 
							contract_no="{contract}", 
							parent_name="{name}", 
							mobile_no="{mobile}"
						WHERE
							name="{mobile}"
						""".format(year=year, branch=branch, contract=contract, name=name, mobile=mobile))
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
		
