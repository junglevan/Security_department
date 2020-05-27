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

/* 拍摄区动态样式 */
$(function () {
    $("#background>#car>#pic>.picOption").on("mouseover", function () {
        $(this).addClass("overed").removeClass("unovered");
    });
    $("#background>#car>#pic>.picOption").on("mouseout", function () {
        $(this).addClass("unovered").removeClass("overed");
    });

    function sendPic(inORout) {
        // alert(inORout);
        var picFile = $("<input type='file'>");
        picFile.click();
        filename = null;
        picFile.on("input", function () {
            // alert("打开了dialog");
            // console.log(picFile.val());
            filename = (picFile.val().split("\\"))[2];
            // console.log(filename);
        });
        
        picFile.on("change", function () {
            var data = {
                "dir": inORout,
                "filename": filename,
            }

            $.ajax({
                url: "/carcheck",
                data: JSON.stringify(data),
                type: 'POST',
                contentType:"application/json;charset=utf-8",
                dataType:"json",
                success: function (respText) {
                    console.log(respText);
                    if (respText.status == 200) {
                        $("#carimg").css("background-image", "url('/static/imgs/main/wellcome.png')");
                    }else if (respText.status == 201) {
                        $("#carimg").css("background-image", "url('/static/imgs/main/bye.jpg')");
                    }else{
                        alert(respText.data);
                        location.href = "/carregister";
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        });
    }

    $("#in").on("click", function () {
        // alert("进入");
        sendPic($(this).prop("id"));
    });

    $("#out").on("click", function () {
        // alert("出去");
        sendPic($(this).prop("id"));
    });

});
