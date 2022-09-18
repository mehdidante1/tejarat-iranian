$(document).ready(function(){

    $(document).on('click' , ".add-to-cartt" , function(){
		$(".P-loader").hide();
        var _vm=$(this);
		//var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-").val();
        var _productId=$(".product-id-").val();
		var _productImage=$(".product-image-").val();
        var _productTitle=$(".product-title-").val();
        var _productPrice=$(".product-price-").text();
        
        // Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
				'image':_productImage,
				'id':_productId,
				'qty':_qty,
				'title':_productTitle,
				'price':_productPrice,	
			},
			dataType:'json',
			beforeSend:function(){
				$(".P-loader").show();
				_vm.attr('disabled',true);
			},
			success:function(res){
				console.log(res);
				_vm.attr('disabled',false);
				$("#cartlist").html(res.data);
				$(".P-loader").hide();
			}
		});
		// End
    })
});
