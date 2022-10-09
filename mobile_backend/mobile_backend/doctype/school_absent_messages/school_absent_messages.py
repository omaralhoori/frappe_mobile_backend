# Copyright (c) 2022, Omar and contributors
# For license information, please see license.txt

import json
from mobile_backend.mobile_backend.doctype.school_messaging.school_messaging import add_messages
import frappe
from frappe.model.document import Document
from dateutil import parser
import requests
from xml.etree import ElementTree

class SchoolAbsentMessages(Document):
	pass
													

@frappe.whitelist()
def get_messages(date):
	settings = frappe.get_single("School Settings")
	formatted_date = parser.parse(date).strftime("%d%m%Y")
	url = f"{settings.data_url}/reports/rwservlet?report=STRMOBABS&userid={settings.user_id}&PDATE={formatted_date}"
	res = requests.get(url)
	absent_list = []
	tree = ElementTree.fromstring(res.content)
	for absent in tree.findall("Absent"):
		try:
			absent_list.append({
				"msg": absent.find("MSG").text,
				"branch_code": absent.find("BRNCOD").text,
				"student_name": absent.find("STDNAME").text,
				"contract_no": absent.find("CONNO").text, 
				"student_no": absent.find("STDNO").text, 
				"class_code": absent.find("CLASSCODE").text, 
				"section_code": absent.find("DIVCODE").text, 
				"class_name": absent.find("CLASSNAME").text, 
				"section_name": absent.find("DIVNAME").text, 
			})
		except:
			frappe.throw("Unable to get messages!")
	return absent_list

@frappe.whitelist()
def send_messages(messages):
	messages = json.loads(messages)
	res = add_messages(messages, "School Group Message", "تقرير غياب")
	return res