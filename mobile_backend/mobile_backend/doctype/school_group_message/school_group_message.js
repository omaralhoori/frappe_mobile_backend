// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Group Message', {
	refresh: function(frm) {
		frm.set_query("branch", function() {
			return {
				query: "mobile_backend.controllers.data_query.branch_query"
			};
		});
		frm.set_query("class_code", function() {
			return {
				query: "mobile_backend.controllers.data_query.class_query"
			};
		});
		
		frm.set_query("section", function() {
			return {
				query: "mobile_backend.controllers.data_query.section_query",
				filters: [
					["class", "=", frm.doc.class_code]
				]
			}
		});
		

	}
});
