$(document).ready(function(){

    //add address

    $(document).on('click','.active-address',function(){
		var _aId=$(this).attr('data-address');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
                if(res.bool == true){
                    $(".check").hide();
                    $(".actbtn").show();
                    
                    $(".check"+_aId).show();
                    $(".btn"+_aId).hide();
                }
			
			}
		});
		// End
	});
    //end
});
