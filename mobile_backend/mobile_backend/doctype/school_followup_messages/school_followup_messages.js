// Copyright (c) 2022, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Followup Messages', {
	// refresh: function(frm) {

	// }
	get_messages: function(frm){
		if (!frm.doc.voucher_no){
			frappe.throw("Please Enter Voucher No")
		}
		frappe.call({
			"method": "mobile_backend.mobile_backend.doctype.school_followup_messages.school_followup_messages.get_messages",
			args: {
				"voucher_no": frm.doc.voucher_no
			},
			callback: (res) => {
				if (res.message){
					frm.set_value("messages", [])
					for(var followup of res.message){
						var row = frm.add_child("messages");
						row.message = followup.msg;
						row.branch_code = followup.branch_code;
						row.contract_no = followup.contract_no;
						row.student_no = followup.student_no;
					}
					frm.refresh_fields("messages");
				}
			}
		})
	},
	send_messages: function(frm){
		var messages = frm.doc.messages.map(absent => {
			return {
				branch_code: absent.branch_code,
			contract_no: absent.contract_no,
			student_no: absent.student_no,
			message: absent.message,
			};
		})
		frappe.call({
			method: "mobile_backend.mobile_backend.doctype.school_followup_messages.school_followup_messages.send_messages",
			args: {
				messages: messages
			},
			callback: function(res){
				if(res.message == 1){
					frappe.show_alert({
						message:__('Messages have been sent successfully.'),
						indicator:'green'
					}, 5);
					frm.set_value("status", "Sent")
					frm.save()
				}else if(res.message == 2){
					frappe.show_alert({
						message:__('Sending messages...'),
						indicator:'green'
					}, 5);
					frm.set_value("status", "Sent")
					frm.save()
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
