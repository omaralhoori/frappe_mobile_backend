from __future__ import unicode_literals
import frappe
import requests
import json

@frappe.whitelist()
def update_device_token():
    user = frappe.session.user
    token = frappe.form_dict.device_token
    frappe.db.set_value("School Parent", user, {"device_token":token})
    frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def send_notification():
    branch = frappe.form_dict.branch
    year = frappe.form_dict.year
    contract = frappe.form_dict.contract
    title = frappe.form_dict.title
    message = frappe.form_dict.message
    token = frappe.db.get_value("School Parent", {
        "branch": branch,
        "year": year,
        "contract_no": contract
    }, ["device_token"])
    if token:
        return send_parent_notification(token, title, message)
    else:
        return "token not found"


def send_parent_notification(token, title, message):
    if not frappe.local.conf.fcm_server_key:
        return "Firebase Cloud Messaging API Key is not set"
    if not token:
        return
    headers = {
        'Content-Type': 'application/json',
        'Authorization': frappe.local.conf.fcm_server_key,
      }
    body = {
          'notification': {'title': title,
                            'body': message},
          'to':
              token,
          'priority': 'high',}
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    return response.json()