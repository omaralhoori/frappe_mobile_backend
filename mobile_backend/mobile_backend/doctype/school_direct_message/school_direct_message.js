// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Direct Message', {
	refresh: function(frm) {
		frm.set_query("branch", function() {
			return {
				query: "mobile_backend.controllers.data_query.branch_query"
			};
		});
		frm.set_query("parent_no", function() {
			return {
				query: "mobile_backend.controllers.data_query.parent_query",
				filters: [
					["branch", "=", frm.doc.branch],
					["year", "=", frm.doc.year],
				]
			};
		});
	}
});
