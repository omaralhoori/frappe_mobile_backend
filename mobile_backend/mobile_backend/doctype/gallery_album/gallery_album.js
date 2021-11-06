// Copyright (c) 2021, Omar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gallery Album', {
	refresh: function(frm) {
		let attachments = frm.attachments.get_attachments();
		let image_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'jfif', 'tiff', 'gif'];
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
	},
	onload: function(frm){
		// if(!frm.is_new()){
		// 	if(!frm.images_uploader){
		// 		var images_area = $(`<div />`)
		// 			.appendTo(frm.fields_dict.images.wrapper);
		// 		frm.images_input = $(`<input type="file" name="files" style="display: none;"
		// 		 accept="image/png, image/jpeg" multiple />`).appendTo(images_area)

		// 		 frm.images_input.change(e => {
		// 			let files = frm.images_input.prop('files')
		// 			console.log(files);
		// 			for (let i=0; i < files.length; i++){
		// 				let file = files[i]
		// 				if (typeof file != 'number'){
		// 					frm.attachments.add_attachment(file);
		// 				}
		// 			}	
		// 		 })
		// 	}else{
		// 		frm.images_uploader.show();
		// 	}
		// }
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
