$(function(){


  $(".btn.deploy").click(function(){
    var $button = $(this);
    var data = {deployable:$(this).attr("data-deployable"),
                target:$(this).attr("data-target")};

    $button.siblings("div.result").html("deploying...");

    $.ajax("/deploy", {method:"POST", 
                       data:data,
                       success:function(res){
                         
                         console.log(res);
                         $button.siblings("div.result").html(res);

                       }});
                       

  });


});
