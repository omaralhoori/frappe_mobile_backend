frappe.listview_settings['School Followup Messages'] = {
add_fields: ["status"],
	get_indicator(doc) {
		if(doc.status=="Sent") {
			return [__("Sent"), "green", "status,=,sent"];
		} else if(doc.status=="Not Sent") {
			return [__("Not Sent"), "orange", "status,=,Not Sent"];
		}
	},
	hide_name_column: true,
	onload: function(listview){
		listview.page.add_button("Get Followups", () => {
			frappe.call({
				method: "mobile_backend.mobile_backend.doctype.school_followup_messages.school_followup_messages.get_vouchers"
			})
		})
	}
}