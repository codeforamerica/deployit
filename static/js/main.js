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


  $(".list.commit").each(function(i, el){

    $.ajax("/currentCommits", 
      {data:{deployable:$(el).attr("data-deployable")},
      dataType:"json",
       success: function(commits){
        for (var c in commits) {
          commit_title = $("<dt></dt>").text(commits[c].message);
          commit_desc = $("<dd></dd>").text(commits[c].author +' '+ 
            commits[c].date);
          $(el).append(commit_title, commit_desc);
        }}
      })


  });





});
