$(document).ready(function(){
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
    // cn 指的是【下阶段应该填写的期数】， 将文本覆盖为 已完成
    $("#cn").after(function(){
        // alert($(this).text()[1]);
        // 获取当前期数
        var num;
        if ($(this).text() === "completed"){
            num = 7
        }
        else{
            num = $(this).text()[1];
            // alert($("#wj" + num).text());
        }
        $(this).remove();
        for (var i=1;i<num;i++){
            // alert(123);
            // alert($("#wj" + i).text());
            $("#wj" + i).text("已完成")
        }
        // 必须要顺序执行
        // 获取链接,如果有连接，则将链接转接
        // alert($("#lj").size() > 0);
        if ($("#lj").size() > 0){
            lj = $("#lj");
            // 链接赋予链接
            $("#wj" + num).wrap("<a href=" + lj.attr("href")+" ></a>");
            //删除链接
            lj.remove();
        }
    });
    // 【False】 转换为【未填写】
    $(".bool").after(function(){
        // alert($(this).text());
        if ($(this).text() === 'False'){
            $(this).text("未到填写时间");
        }
    });
});