// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Student', {
	refresh: function(frm) {
		frm.add_custom_button(__('Payments'), function(){
			if(frm.doc.branch && frm.doc.year && frm.doc.contract_no && frm.doc.student_no)
				window.open(`/transaction_report?PBRN=${frm.doc.branch}&PYEAR=${frm.doc.year}&PCONNO=${frm.doc.contract_no}&PSTD=${frm.doc.student_no}`, '_blank').focus();
		  });
	}
});
