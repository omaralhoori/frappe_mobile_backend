# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "mobile_backend"
app_title = "Mobile Backend"
app_publisher = "Omar"
app_description = "Mobile Backend"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mobile_backend@frappe.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mobile_backend/css/mobile_backend.css"
# app_include_js = "/assets/mobile_backend/js/mobile_backend.js"

# include js, css files in header of web template
# web_include_css = "/assets/mobile_backend/css/mobile_backend.css"
# web_include_js = "/assets/mobile_backend/js/mobile_backend.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "mobile_backend.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mobile_backend.install.before_install"
# after_install = "mobile_backend.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mobile_backend.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mobile_backend.tasks.all"
# 	],
# 	"daily": [
# 		"mobile_backend.tasks.daily"
# 	],
# 	"hourly": [
# 		"mobile_backend.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mobile_backend.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mobile_backend.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mobile_backend.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mobile_backend.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mobile_backend.task.get_dashboard_data"
# }

