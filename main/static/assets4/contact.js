$(document).ready(function(){
    $(document).on('submit' , '#tamasbama' , function(e){
        e.preventDefault();
    
        $.ajax({
            type : 'POST',
            url : '/tamas',
            data : {
                name : $('#name').val(),
                email : $('#email').val(),
                phone : $('#phone').val(),
                subject : $('#subject').val(),
                text : $('#text').val(),
                csrfmiddlewaretoken:$('input[name = csrfmiddlewaretoken]').val(),
            },
            success : function(){
                alert("نظر شما با موفقیت ثبت شد.");
            }
        });
    
    });
});
