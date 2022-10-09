// Copyright (c) 2022, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Claim Messages', {
	refresh: function(frm) {
		frm.disable_save();
	},
	get_messages: function(frm){
		if (!frm.doc.date){
			frappe.throw("Please Select The Date")
		}
		if (!frm.doc.serial){
			frappe.throw("Please Enter Serial")
		}
		frappe.call({
			"method": "mobile_backend.mobile_backend.doctype.school_claim_messages.school_claim_messages.get_messages",
			args: {
				"date": frm.doc.date,
				"serial": frm.doc.serial
			},
			callback: (res) => {
				if (res.message){
					frm.set_value("claim_messages", [])
					for(var claim of res.message){
						var row = frm.add_child("claim_messages");
						row.message = claim.msg;
						row.branch_code = claim.branch_code;
						row.contract_no = claim.contract_no;
					}
					frm.refresh_fields("claim_messages");
				}
			}
		})
	},
	send_messages: function(frm){
		var messages = frm.doc.claim_messages.map(claim => {
			return {
				branch_code: claim.branch_code,
			contract_no: claim.contract_no,
			message: claim.message,
			};
		})
		frappe.call({
			method: "mobile_backend.mobile_backend.doctype.school_claim_messages.school_claim_messages.send_messages",
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
