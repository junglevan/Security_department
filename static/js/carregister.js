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

/* 表单动态样式 */
$(function () {
    /* -----输入框----- */
    var placeholderinfo = {};
    // placeholderinfo[$(this).prop("name")] = $(this).prop("placeholder");
    $(".form-group>input").each(function () {
        placeholderinfo[this.name] = this.placeholder;
    });
    $(".form-group>input").on("focus", function () {
        $(this).css("border-color", "#3485FB");
        if (!$(this).val()) {
            $(this).prop("placeholder", placeholderinfo[$(this).prop("name")]);
        }
    });
    $(".form-group>input").on("blur", function () {
        if (!$(this).val()) {
            $(this).css("border-color", "red").prop("placeholder", "内容不能为空");
        }else{
            $(this).css("border-color", "darkcyan");
        }
    });

    /* -----来访者身份----- */
    $(".form-group>div").on("mouseover", function () {
        $(this).addClass("overed").removeClass("unovered");
    });
    $(".form-group>div").on("mouseout", function () {
        $(this).removeClass("overed").addClass("unovered");
    });
    $("#person>div").on("click", function () {
        $(this).addClass("checked").siblings().removeClass("checked");
    });
});

/* 提交按钮 */
$(function () {
    $("#submit").on("click", function () {
        if ($("#name").val() && $("#address").val() && $("#carId").val()) {
            var data = {
                "name": $("#name").val(),
                "carId": $("#carId").val(),
                "phone": $("#phone").val(),
                "address": $("#address").val(),
                "person": $("#visitor").hasClass("checked") ? "visiters" : "owners",
            };
            $.ajax({
                url: "/carregister",
                data:JSON.stringify(data),
                type:"POST",
                contentType:"application/json;charset=utf-8",
                dataType:"json",
                success: function (respTest) {
                    console.log("返回的信息:", respTest);
                    if (respTest.status == 200) {
                        alert(respTest.data);
                        if (confirm("是否继续注册?")) {
                            location.href = "/carregister";
                        }else{
                            location.href = "/carcheck";
                        }
                    }else{
                        alert(respTest.data);
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }else{
            alert("提供的信息不完整");
        }
    });
});
