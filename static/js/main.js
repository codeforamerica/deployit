$(function(){


  $(".btn.deploy").click(function(){
    var $button = $(this);

    var deployable = $(this).attr("data-deployable");

    $("[data-deployable='"+deployable+"'].results").html("deploying...");

    var params = "deployable="+encodeURIComponent(deployable)+
      "&target="+encodeURIComponent($(this).attr("data-target"));

    var oReq = new XMLHttpRequest();
    oReq.onreadystatechange = function()
    {
      if (this.readyState > 2 && this.status == 200)
      {
        var response = this.responseText;
        console.log(response);
        $("[data-deployable='"+deployable+"'].results").html(response.replace(/\n/g, "<br />"));
      }
    }
    oReq.open("post", "/deploy", true);
    oReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    oReq.send(params);

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
