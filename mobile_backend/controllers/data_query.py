from __future__ import unicode_literals
import frappe

from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique


@frappe.whitelist()
def branch_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	fields = get_fields("School Branch", ["name", "branch_name"])

	return frappe.db.sql("""select {fields} from `tabSchool Branch`
		WHERE ({key} like %(txt)s
				or branch_name like %(txt)s)
			{fcond} {mcond}
        order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, branch_name), locate(%(_txt)s, branch_name), 99999),
			idx desc,
			name, branch_name
		limit %(start)s, %(page_len)s""".format(**{
			'fields': ", ".join(fields),
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})

@frappe.whitelist()
def class_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	page_len = 50
	fields = get_fields("School Class", ["name", "class_name"])

	return frappe.db.sql("""select {fields} from `tabSchool Class`
		WHERE ({key} like %(txt)s
				or class_name like %(txt)s)
			{fcond} {mcond}
        order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, class_name), locate(%(_txt)s, class_name), 99999),
			idx desc,
			name, class_name
		
		limit %(start)s, %(page_len)s""".format(**{
			'fields': ", ".join(fields),
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})
@frappe.whitelist()
def section_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	fields = get_fields("School Section", ["name", "section_name"])

	return frappe.db.sql("""select {fields} from `tabSchool Section`
		WHERE ({key} like %(txt)s
				or section_name like %(txt)s)
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, section_name), locate(%(_txt)s, section_name), 99999),
			idx desc,
			name, section_name
		limit %(start)s, %(page_len)s""".format(**{
			'fields': ", ".join(fields),
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})

@frappe.whitelist()
def parent_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	fields = get_fields("School Parent", ["name", "parent_name"])

	return frappe.db.sql("""select {fields} from `tabSchool Parent`
		WHERE ({key} like %(txt)s
				or parent_name like %(txt)s
				or contract_no like %(txt)s
				)
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, parent_name), locate(%(_txt)s, parent_name), 99999),
			idx desc,
			name, parent_name
		limit %(start)s, %(page_len)s""".format(**{
			'fields': ", ".join(fields),
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})

@frappe.whitelist()
def get_message_types(doctype, txt, searchfield, start, page_len, filters):
	return [("School Direct Message", "School Direct Message"),( "School Group Message",  "School Group Message")]

def get_fields(doctype, fields=None):
	if fields is None:
		fields = []
	meta = frappe.get_meta(doctype)
	fields.extend(meta.get_search_fields())

	if meta.title_field and not meta.title_field.strip() in fields:
		fields.insert(1, meta.title_field.strip())

	return unique(fields)