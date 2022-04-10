# Copyright (c) 2022, Omar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SchoolDegreeReportSettings(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_degree_settings():
	settings = frappe.get_doc('School Degree Report Settings')
	students = frappe.db.sql("""
		SELECT student_no, degree_report FROM `tabSchool Student`
		WHERE parent_no=%s
	""", frappe.session.user, as_dict=True)
	return {
		"first_semester": {
			"first_semester": settings.first_semester,
			"first_period_1": settings.first_period_1,
			"first_period_2": settings.first_period_2,
			"first_period_3": settings.first_period_3,
			"first_period_4": settings.first_period_4,
			"first_all_periods": settings.first_all_periods,
		},
		"second_semester": {
		"second_semester": settings.second_semester,
		"second_period_1": settings.second_period_1,
		"second_period_2": settings.second_period_2,
		"second_period_3": settings.second_period_3,
		"second_period_4": settings.second_period_4,
		"second_all_periods": settings.second_all_periods,
		},
		"students": students
	}