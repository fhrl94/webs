$(document).ready(function(){
    // 真假转换
    $(".bool").after(function(){
        // alert($(this).text());
        if ($(this).text() === 'True'){
            $(this).text("已完成");
        }
        else {
            $(this).text("未到填写时间");
        }
    });
    // cs 指的是【理论应该填写的期数】，将文本覆盖为 待填写
    $("#cs").after(function(){
        // alert($(this).text()[1]);
        var num = $(this).text()[1];
        $(this).remove();
        for (var i=1;i<=num;i++){
            // alert($("#wj" + i).text());
            $("#wj" + i).text("待填写")
        }
    });
    //
    $("#cn").after(function(){
        // alert($(this).text()[1]);
        // 获取当前期数
        var num;
        lj = $("#lj");
        if ($(this).text() === "completed"){
            num = 7
        }
        else{
            num = $(this).text()[1];
            // 新增链接
            // alert($("#wj" + num).text());
            $("#wj" + num).wrap("<a href=" + lj.attr("href")+" ></a>");
        }
        lj.remove();
        $(this).remove();
        for (var i=1;i<num;i++){
            // alert(123);
            // alert($("#wj" + i).text());
            $("#wj" + i).text("已完成")
        }
    });

});