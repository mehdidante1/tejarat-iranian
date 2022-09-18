$(document).ready(function(){
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box product product-type-simple").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box product product-type-simple").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});
	$("choose-size").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
	});
	// End

});
