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
	},
	onload: function(listview){
		listview.page.fields_dict.message_type.get_query = function() {
			return {
				query: "mobile_backend.controllers.data_query.get_message_types"
			};
		};
		$(".primary-action").hide()
	}
};