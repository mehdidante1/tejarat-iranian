$(document).ready(function(){
	$(".choose-size").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color"+_color).first().addClass('active');

		var _price=$(".color"+_color).first().attr('data-price');
		$(".product-price-").text(_price);
	});
	// End

	//show the price according to selected sizes

	$(".choose-size").on('click',function(){
		$(".color"+_color).removeClass('active');
		$(this).addClass('active');
		var _price=$(this).attr('data-price');
		$(".product-price-").text(_price);

	});

	//End

	//show the first selected color
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price');
	
	$(".color"+_color).show();
	$(".color"+_color).first().addClass('active');
	$(".product-price-").text(_price);

});
