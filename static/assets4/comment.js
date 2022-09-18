$(document).ready(function(){

    //review

    $("#addFormComment").submit(function(e){
		$.ajax({
            data : $(this).serialize(),
            method : $(this).attr('method'),
            url : $(this).attr('action'),
            dataType : 'json',
            success:function(res){
                if(res.bool==true){
                    $(".ajaxRess").html("نظر شما با موفقیت ثبت شد.");
                    var _html = '<div id="product-questions-list" >';
                    _html += '<div class="questions-list">'
                    _html += '<ul class="faq-list">';
                    _html += '<li class="is-question">';
                    _html += '<div class="section">';
                    _html += '<div class="faq-header">';
                    _html += '<span class="icon-faq">?</span>';
                    _html += '<p class="h5">';
                    _html += ' پرسش :';
                    _html += ' <span>'+res.data.name+' '+res.data.family+'</span>';
                    _html += '</p>';
                    _html += '</div>';
                    _html += '<p>'+res.data.text_comment+'</p>';
                    _html += '<div class="faq-date">';
                    _html += '<em></em>';
                    _html += '</div>';
                    _html += ' <a href="#" class="js-add-answer-btn">به این پرسش پاسخ دهید </a>';
                    _html += '</div>';
                    _html += '</li>';
                    _html += '</ul>';
                    _html += '</div>';
                    _html += '</div>';
                    $(".review-list").prepend(_html);
                    $("#exampleModal-comment").modal('hide');
                    $("#addFormComment").trigger('reset');
                    
                }
            } 
        });
        e.preventDefault();
	});
    //end
});
