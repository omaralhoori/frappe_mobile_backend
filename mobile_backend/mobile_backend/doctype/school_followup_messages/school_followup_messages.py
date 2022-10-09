# Copyright (c) 2022, Omar and contributors
# For license information, please see license.txt

import json

from mobile_backend.mobile_backend.doctype.school_messaging.school_messaging import add_messages
import frappe
from frappe.model.document import Document
import requests
from xml.etree import ElementTree
from dateutil import parser

class SchoolFollowupMessages(Document):
	pass


@frappe.whitelist()
def get_vouchers():
	settings = frappe.get_single("School Settings")
	url = f"{settings.data_url}/reports/rwservlet?report=STRMOBFLWG&userid={settings.user_id}"

	res = requests.get(url)

	followup_list = []
	tree = ElementTree.fromstring(res.content)
	for followup in tree.findall("FollowupList"):
		try:
			followup_list.append({
				"voucher_no": followup.find("VOUCHERNO").text,
				"from_date": parser.parse(followup.find("FROMDATE").text),
				"to_date": parser.parse(followup.find("TODATE").text),
			})
		except:
			frappe.throw("Unable to get messages!")
	for followup in followup_list:
		if not frappe.db.exists("School Followup Messages", followup):
			followup["doctype"] = "School Followup Messages"
			doc = frappe.get_doc(followup)
			doc.insert()
	
	frappe.db.commit()

@frappe.whitelist()
def get_messages(voucher_no):
	settings = frappe.get_single("School Settings")
	url = f"{settings.data_url}/reports/rwservlet?report=STRMOBFLW&userid={settings.user_id}&PVOUCHERNO={voucher_no}"

	res = requests.get(url)

	followup_list = []
	tree = ElementTree.fromstring(res.content)
	for followup in tree.findall("FollowupList"):
		try:
			followup_list.append({
				"branch_code": followup.find("BRNCODE").text,
				"contract_no": followup.find("CONNO").text,
				"student_no": followup.find("STDNO").text,
				"msg": followup.find("MSG").text,
				
			})
		except:
			frappe.throw("Unable to get messages!")
	return followup_list


@frappe.whitelist()
def send_messages(messages):
	messages = json.loads(messages)
	res = add_messages(messages, "School Group Message", "تقرير متابعة الطالب")
	return res