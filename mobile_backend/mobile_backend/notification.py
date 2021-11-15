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
        return send_token_notification(token, title, message)
    else:
        return "token not found"


def send_multiple_notification(tokens, title, message, data=None):
    if not tokens or len(tokens) == 0:
        return
    body = {
          'notification': {'title': title,
                            'body': message},
          'registration_ids':
              tokens,
          'priority': 'high',}
    if data:
        body["data"] = data
    return send_http_notification(body)

def send_token_notification(token, title, message, data=None):
    if not token:
        return
    body = {
          'notification': {'title': title,
                            'body': message},
          'to':
              token,
          'priority': 'high',}
    if data:
        body["data"] = data
    return send_http_notification(body)


def send_topic_notification(topic, title, message, data=None):
    body = {
          'notification': {'title': title,
                            'body': message},
          'to': '/topics/' + topic,
          'priority': 'high',}
    if data:
        body["data"] = data
    return send_http_notification(body)

def send_http_notification(body):
    if not frappe.local.conf.fcm_server_key:
        return "Firebase Cloud Messaging API Key is not set"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': frappe.local.conf.fcm_server_key,
      }
    data = json.dumps(body)
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=data)
    return response