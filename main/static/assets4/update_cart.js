$(document).ready(function(){

    //update item from cart
	//$(".P-loader").hide();
    $(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
        var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
                'qty' : _pQty,
			},
			dataType:'json',
			beforeSend:function(){
				//$(".P-loader").show();
				_vm.attr('disabled',true);
			},
			success:function(res){
				//$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartlist").html(res.data);
                //$(".P-loader").hide();
			}
		});
		// End
	});
    //end
});
