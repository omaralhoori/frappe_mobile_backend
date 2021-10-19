// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contact Messages', {
	refresh: function(frm) {
		frm.page.menu.find("a:contains("+__("Email")+")").on('click', function() {
           setTimeout(() => {
               $('*[data-fieldname="subject"]').val(frm.doc.subject)
           },500); 
        });
	}
});
