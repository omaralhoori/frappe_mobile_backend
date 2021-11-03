// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('School Messaging', {
	refresh: function(frm) {
		frm.set_query("message_type", function() {
			return {
				query: "mobile_backend.controllers.data_query.get_message_types"
			};
		});
		frm.set_query("branch", function() {
			return {
				query: "mobile_backend.controllers.data_query.branch_query"
			};
		});
		frm.set_query("parent_name", function() {
			return {
				filters: [
					["branch" , "=", frm.doc.branch]
				]
			};
		});

		if ($(frm.fields_dict.messaging_container.wrapper).html() == ''){
			messaging_container(frm.fields_dict.messaging_container.wrapper, frm);

			
		}
		if(frm.doc.messages){
			let messages_wrapper = $(frm.fields_dict.messaging_container.wrapper).find('.messages-wrapper')
			messages_wrapper.html('')
			for(let message of frm.doc.messages){
				add_message(frm, messages_wrapper, message.name, message.message, message.sender_name, message.is_read, message.is_administration, message.sending_date)
			}
		}
		
		update_status(frm);
		$('.admin-message.viewed:last i').css({"display": "inline-block"});
	}
});

let update_status = (frm) => {
	if(frm.doc.status == 'Not seen')
		{
			frm.set_value('status', "Seen");
			for(let message of frm.doc.messages){
				if(message.is_administration == 0){
					message.is_read = 1;
				}
			}
			frm.save();
		}
}


let messaging_container = (wrapper, frm) => {
	let messaging_wrapper = $(`
	<div class="messaging-wrapper">
		<div class="messages-wrapper"></div>
		<div class="messaging-header"> 
		<label>Send Message</label>
		<button class="send-button btn">${__('Send')}</button>
		</div>
		<div class="control-input messaging-body">
			<textarea rows="5" class="input-with-feedback form-control bold"> </textarea>
		</div>
	</div>
	`).appendTo(wrapper);
	let messages_wrpper = messaging_wrapper.find('.messages-wrapper')
	messaging_wrapper.find('button').click( () => {
		let message = messaging_wrapper.find('textarea').val();
		messaging_wrapper.find('textarea').val('');
		console.log(message);
		let row = frm.add_child("messages")
		row.sender_name = 'Administration'
		row.message = message;
		row.is_administration = 1;
		row.sending_date = dateutil.now_datetime();
		//add_message(messages_wrpper, message, 'Administration', 1, 1)
		refresh_field("messages")
		frm.save();
	})
}


let add_message = (frm, wrapper, name, msg, sender, is_read, is_admin, sending_date) => {
	let msg_class = is_admin ? 'admin-message' : 'user-message';
	msg_class += is_read ? ' viewed' : ''
	let delete_btn = wrapper.html() != '' ? '<button class="delete-message">&times;</button>' : ''
	let msg_wapper = $(`<div class="message-wrapper ${msg_class}">
		<div class="sender">${sender}</div>
		<div class="sending-date">${sending_date}</div>
		<div class="message-btn">
		<div class="message">
			</div>
			<i class="fa fa-eye"></i>
			${delete_btn}
		</div>
	</div>`).appendTo(wrapper)
	msg_wapper.find('.message').text(msg)
	msg_wapper.find('.delete-message').click(() => {
		//var tbl = frm.doc.messages || [];
		msg_wapper.html('');
		// for(let i=0; i<tbl.length; i++){
		// 	if(tbl[i].name == name)
		// 		{
		// 			frm.get_field("messages").grid.grid_rows[i].remove();
		// 			break;
		// 		}
		// }
		frm.doc.messages = frm.doc.messages.filter(message => {
			if(message.name == name)
				return false;
			return true;
		})
		refresh_field("messages")
		frm.save()
	})
}