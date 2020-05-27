/* 导航栏动态样式 */
$(function () {
    $("#top>#nav>div").on("mouseover", function () {
        $(this).addClass("menushow").removeClass("menuhide");
    });
    $("#top>#nav>div").on("mouseout", function () {
        if (!$(this).hasClass("isActive")) {
            $(this).removeClass("menushow").addClass("menuhide");
        }else{
            $(this).removeClass("menushow").addClass("isActive");
        }
    });
});
