$(document).ready(function(){
    $.ajax({
        url:'/notifs',
        datatype:'json',
        beforeSend:function(){  
        },
        success:function(res){
            _html='';
            _json=$.parseJSON(res.data);
            $.each(_json , function(index,d){
                console.log(d);
            });         
        } 
    });
});
