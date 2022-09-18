$(document).ready(function(){

    $(document).on('click' , ".add-to-cartt" , function(){
		$(".P-loader").hide();
        var _vm=$(this);
		var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productId=$(".product-id-"+_index).val();
		var _productImage=$(".product-image-"+_index).val();
        var _productTitle=$(".product-title-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();
        
        // Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
				'id':_productId,
				'image':_productImage,	
				'qty':_qty,
				'title':_productTitle,
				'price':_productPrice
				
			},
			dataType:'json',
			beforeSend:function(){
				$(".P-loader").show();
				_vm.attr('disabled',true);
			},
			success:function(res){
				$("#cartlist").text(res.totalitems);
				_vm.attr('disabled',false);
				$(".P-loader").hide();
			}
		});
		// End
    })
});
