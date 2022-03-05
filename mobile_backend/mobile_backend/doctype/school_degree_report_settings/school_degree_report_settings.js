// Copyright (c) 2022, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Degree Report Settings', {
	refresh: (frm) => {
		toggle_periods(frm, "first");
		toggle_periods(frm, "second");
	},
	first_semester: function(frm){
		toggle_periods(frm, "first");
	},
	second_semester: function(frm){
		toggle_periods(frm, "second");
	},
	
});

const toggle_periods = function(frm, semester){
	frm.toggle_display(`${semester}_periods_section`, frm.doc[`${semester}_semester`]== 1);
}