$(document).ready(function(){

    $(document).on('change', '#post-form',function(e){
        e.preventDefault();
        $.ajax({
            
            url:'/ajaxcolor',
            data:{
                productid:$('#productid').val(),
                size:$('#size').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            data_type : 'html',
            success: function (data) {
                console.log("success");
                $('#appendHere').html(data.rendered_table);
            },
            error: function (data) {
                alert("Got an error dude " + data);
            }
        });
    });
    //end
});




























