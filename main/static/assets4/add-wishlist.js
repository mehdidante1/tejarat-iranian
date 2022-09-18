$(document).ready(function(){

    //review

    $(".add-wishlist").on('click' , function(){

        var _pid = $ (this).attr('data-product');
        var _vm=$(this);
		$.ajax({
           url:"/add-wishlist",
           data:{
               product : _pid
           },
           datatype :'json',

           success:function(res){
               if(res.bool==true){
                   _vm.addClass('disabled').removeClass('add-wishlist');
               }
               //alertify.success(res.status)
           }
        });
        
	});
    //end
});
