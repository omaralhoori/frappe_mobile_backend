// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Import School Data', {
	before_load: function(frm) {
		frm.disable_save();
	},
	// refresh: function(frm) {

	// },
	import_branch_data: function(frm){
		frappe.show_progress("Importing", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "import_branch_data",
			args: {
				//url: frm.doc.branch_url
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
				//url: frm.doc.year_url
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
				//url: frm.doc.class_url
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
				//url: frm.doc.section_url
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
				branch: frm.doc.parent_branch,
				year: frm.doc.parent_year,
				password: frm.doc.default_password,
				set_password: frm.doc.set_password,
				update_exists: frm.doc.update_exists
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
				branch: frm.doc.student_branch,
				year: frm.doc.student_year,
			},
			callback: (res) => {
				frappe.hide_progress();
			}
		})
	},
	change_password_button: function(frm){
		frappe.confirm(__('Are you sure you want to change the password for all parents in the selected branch?'),
    () => {
        frappe.show_progress("Processing...", 1, 2)
		frappe.call({
			doc:frm.doc,
			method: "update_parent_password",
			args: {
				branch: frm.doc.parent_branch,
				year: frm.doc.parent_year,
				update_exists: frm.doc.update_exists_2
			},
			callback: (res) => {
				frappe.show_progress("Processing...", 2, 2)
				frappe.hide_progress();
			}
		})
    }, () => {
        // action to perform if No is selected
    })
		
	},
});
