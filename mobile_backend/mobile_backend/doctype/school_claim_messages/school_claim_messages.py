# Copyright (c) 2022, Omar and contributors
# For license information, please see license.txt

from mobile_backend.mobile_backend.doctype.school_messaging.school_messaging import add_messages
import frappe
from frappe.model.document import Document
import requests
from xml.etree import ElementTree
from dateutil import parser
import json

class SchoolClaimMessages(Document):
	pass



@frappe.whitelist()
def get_messages(date, serial):
	settings = frappe.get_single("School Settings")
	formatted_date = parser.parse(date).strftime("%d%m%Y")
	url = f"{settings.data_url}/reports/rwservlet?report=STRMOBCLM&userid={settings.user_id}&PDATE={formatted_date}&PSERIAL={serial}"
	res = requests.get(url)
	claim_list = []
	tree = ElementTree.fromstring(res.content)
	for claim in tree.findall("ClaimMsg"):
		try:
			claim_list.append({
				"msg": claim.find("MSGTXT").text,
				"branch_code": claim.find("BRN").text,
				"contract_no": claim.find("CONNO").text, 
			})
		except:
			frappe.throw("Unable to get messages!")
	return claim_list

@frappe.whitelist()
def send_messages(messages):
	messages = json.loads(messages)
	res = add_messages(messages, "School Direct Message", "تقرير دفعات")
	return res