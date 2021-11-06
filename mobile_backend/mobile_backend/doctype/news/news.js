// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('News', {
	refresh: function(frm) {
		let attachments = frm.attachments.get_attachments();
		let image_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'jfif', 'tiff', 'gif', 'jpe'];
		$(frm.fields_dict.images.wrapper).html('')
		for (let i in attachments){
			let attachment = attachments[i];
			let fname = attachment.file_name.split('.')
			if (image_extensions.includes(fname[fname.length - 1].toLowerCase())){
				$(`<div class="image-card">
					<div class="card-body"> 
					<img src="${attachment.file_url}"/>
					</div>
				</div>`).appendTo(frm.fields_dict.images.wrapper)
			}
		}
	},
	upload_images: function(frm){
		//frm.images_input.trigger('click');
		if(frm.is_new()){
			frm.save().then(() => {
				frappe.add_attachment(frm);
			})
		}else{
			frappe.add_attachment(frm)
		}
	}
});

frappe.add_attachment = (frm) => {
	//frm.attachments.new_attachment()
	frm.fields_dict.attach.on_attach_click()
}
