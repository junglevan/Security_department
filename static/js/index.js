
$(function () {
    /* 鼠标移动到导航栏中 */
    $("#background>#hrefs>div").on("mouseover", function () {
        $(this).css("background-color", "rgba(120,120,120,0.8)");
    });    

    /* 鼠标移出导航栏 */
    $("#background>#hrefs>div").on("mouseout", function () {
        $(this).css("background-color", "rgba(0,0,0,0.6)");
    });    
});
