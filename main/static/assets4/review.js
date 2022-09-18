$(document).ready(function(){

    //review

    $("#addForm").submit(function(e){
        
		$.ajax({
            data : $(this).serialize(),
            method : $(this).attr('method'),
            url : $(this).attr('action'),
            dataType : 'json',
            success:function(res){
                if(res.bool==true){
                    $(".ajaxRes").html("نظر شما با موفقیت ثبت شد.");
                    $("#resete").trigger('click');

                    //avg rating
                    $(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
                }
            } 
        });
        e.preventDefault();
	});
    //end
});
