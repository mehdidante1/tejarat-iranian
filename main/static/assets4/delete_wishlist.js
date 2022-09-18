$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-book').modal('show');
			},
			success: function(data){
				$('#modal-book .modal-content').html(data.html_form);
			}
		});
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('#wishlist-modal tbody').html(data.book_list);
					$('#modal-book').modal('hide');
				} else {
					$('#wishlist-modal .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}


//delete
$('#wishlist-modal').on("click",".show-form-delete",ShowForm);
$('#modal-book').on("submit",".delete-form",SaveForm)
});