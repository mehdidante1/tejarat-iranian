$(document).ready(function(){

    //delete item from cart

    $(document).on('click','.delete-item',function(){
		$(".P-loader").hide();
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				$(".P-loader").show();
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartlist").html(res.data);
				$(".P-loader").hide();
			}
		});
		// End
	});
    //end
});
