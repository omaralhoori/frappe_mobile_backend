from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
	data = [
		{
			"label": _("Mobile Data"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Announcement",
					"label": _("Announcements"),
				},	
				{
					"type": "doctype",
					"name": "News",
					"label": _("News"),
				},	
				{
					"type": "doctype",
					"name": "Gallery Album",
					"label": _("Gallery"),
				},	
				
			]
		},
		{
			"label": _("School Data"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "School Branch",
					"label": _("Branches"),
				},	
				{
					"type": "doctype",
					"name": "School Year",
					"label": _("Years"),
				},	
				{
					"type": "doctype",
					"name": "School Class",
					"label": _("Classes"),
				},	
				{
					"type": "doctype",
					"name": "School Section",
					"label": _("Sections"),
				},	
				{
					"type": "doctype",
					"name": "School Parent",
					"label": _("Parents"),
				},	
				
			]
		},
		{
			"label": _("Users"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "User",
					"label": _("Mobile Users"),
				},	
				{
					"type": "doctype",
					"name": "Mobile Guest",
					"label": _("Mobile Guests"),
				},	
				
			]
		},
		{
			"label": _("Communication"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Contact Messages",
					"label": _("Contact Messages"),
				},	
				
			]
		},
		{
			"label": _("Tools"),
			"icon": "fa fa-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Comment Manager",
					"label": _("Comment Manager"),
				},	
				{
					"type": "doctype",
					"name": "Import School Data",
					"label": _("Import School Data"),
				},	
				
			]
		},
	]
	return data
