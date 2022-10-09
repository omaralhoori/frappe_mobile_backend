// Copyright (c) 2022, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Absent Messages', {
	refresh: function(frm) {
		frm.disable_save();
	},
	get_messages: function(frm){
		if (!frm.doc.date){
			frappe.throw("Please Select The Date")
		}
		frappe.call({
			"method": "mobile_backend.mobile_backend.doctype.school_absent_messages.school_absent_messages.get_messages",
			args: {
				"date": frm.doc.date
			},
			callback: (res) => {
				if (res.message){
					frm.set_value("absentee_list", [])
					for(var absent of res.message){
						var row = frm.add_child("absentee_list");
						row.student_name = absent.student_name;
						row.class_name = absent.class_name;
						row.section_name = absent.section_name;
						row.message = absent.msg;
						row.section_code = absent.section_code;
						row.class_code = absent.class_code;
						row.branch_code = absent.branch_code;
						row.contract_no = absent.contract_no;
						row.student_no = absent.student_no;
					}
					frm.refresh_fields("absentee_list");
				}
			}
		})
	},
	send_messages: function(frm){
		var messages = frm.doc.absentee_list.map(absent => {
			return {
				branch_code: absent.branch_code,
			contract_no: absent.contract_no,
			student_no: absent.student_no,
			message: absent.message,
			};
		})
		frappe.call({
			method: "mobile_backend.mobile_backend.doctype.school_absent_messages.school_absent_messages.send_messages",
			args: {
				messages: messages
			},
			callback: function(res){
				if(res.message == 1){
					frappe.show_alert({
						message:__('Messages have been sent successfully.'),
						indicator:'green'
					}, 5);
				}else if(res.message == 2){
					frappe.show_alert({
						message:__('Sending messages...'),
						indicator:'green'
					}, 5);
				}
				else{
					frappe.show_alert({
						message:__('Something went wrong.'),
						indicator:'red'
					}, 5);
				}
			}
		})
	}
});
