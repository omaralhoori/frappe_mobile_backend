// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Comment Manager', {
	before_load: function (frm) {
		frm.disable_save();

	},
	get_comments: function(frm){
		var progress = frappe.show_progress(__("Proccessing"), 1, 2, __("Please wait"), true)
		frm.call({
			doc:frm.doc,
			method: "get_comments",
			args:{
				document: frm.doc.document,
				status: frm.doc.status
			},
			callback: function(r, rt) {
				var porgress2 = frappe.show_progress("Proccessing", 2, 2)
				porgress2.hide()
				porgress2.cancel()
				
				progress.cancel();
				progress.hide();
				frappe.hide_progress();
			}
		});
	},
	set_status: function(frm){
		var progress = frappe.show_progress(__("Proccessing"), 1, 2, __("Please wait"), true)
		let comments = frm.doc.comments.map(comment => {
			comment.status = frm.doc.new_status;
			return comment.name
		})
		return frm.call({
			doc:frm.doc,
			method: "set_status",
			args: {
				comments: comments,
				new_status: frm.doc.new_status,
				document: frm.doc.document
			},
			callback: function(r, rt) {
				var porgress2 = frappe.show_progress("Proccessing", 2, 2)
				porgress2.hide()
				porgress2.cancel()
				
				progress.cancel();
				progress.hide();
				frappe.hide_progress();
			}
		});
	}
});
