// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.listview_settings['School Messaging'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
		if(doc.status == 'Seen') {
			return [__("Seen"), "green", "enabled,=,1"];
		} else {
			return [__("Not seen"), "orange", "enabled,=,0"];
		}
	}
};