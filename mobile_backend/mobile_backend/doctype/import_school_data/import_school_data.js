// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Import School Data', {
	// refresh: function(frm) {

	// },
	// refresh: function(frm) {

	// },
	import_branch_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_branch_data",
			args: {
				url: frm.doc.branch_url
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	import_year_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_year_data",
			args: {
				url: frm.doc.year_url
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	import_class_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_class_data",
			args: {
				url: frm.doc.class_url
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	import_section_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_section_data",
			args: {
				url: frm.doc.section_url
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	import_parent_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_parent_data",
			args: {
				url: frm.doc.parent_url,
				password: frm.doc.default_password,
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	import_student_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_student_data",
			args: {
				url: frm.doc.student_url
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
});
