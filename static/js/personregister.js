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

/* 拍摄区动态样式 */
$(function () {
    $("#background>#video>#openCamera, #takeShot,.picOption").on("mouseover", function () {
        $(this).addClass("overed").removeClass("unovered");
    });
    $("#background>#video>#openCamera, #takeShot,.picOption").on("mouseout", function () {
        $(this).addClass("unovered").removeClass("overed");
    });

    var video = document.getElementsByTagName("video")[0];
    var camareStream = null;

    function closeCamare(stream){
        stream.getTracks().forEach(function (track) {
            track.stop();
        });
        }

    function showVideo(video) {
        var config = {video:true, audio:false};

        function success(stream) {
            // console.log(stream);
            if ("srcObject" in video) {
                // console.log("srcObject is in video");
                camareStream = stream;
                video.srcObject = stream;
            }else{
                // console.log("no srcObject");
                var url = window.URL || window.webkitURL;
                video.src = url ? url.createObjectURL(stream) : stream;
            }
            video.addEventListener("canplay", function (ev) {
                // console.log(ev);
                if (stream.active) {
                    video.play();
                }
            }, false);
        }

        function error(err) {
            console.log("错误：", err);
        }

        if (navigator.getUserMedia) {
            // console.log("navigator.getUserMedia");
            navigator.getUserMedia(config,success, error); 
        }else{
            // console.log("navigator.mediaDevices.getUserMedia");
            navigator.mediaDevices.getUserMedia(config,success, error);
        }
    }

    function getShot(video) {
        var picShot = document.createElement("canvas");
        picShot.width = video.width;
        picShot.height = video.height;
        picShot.getContext("2d").drawImage(video, 0, 0, video.width, video.height);
        var imgdata = picShot.toDataURL("image/png");
        console.log(imgdata);
        $("#pic>img")[0].src = imgdata;
    }

    $("#background>#video>#openCamera").on("click", function () {
        $(this).addClass("hide");
        $("#takeVideo").removeClass("hide");
        showVideo(video);
    });

    $("#takeShot").on("click", function () {
        getShot(video);
        $("#takeVideo").addClass("hide");
        $("#pic").removeClass("hide");
        closeCamare(camareStream);        
    });

    $("#accept").on("click", function () {
        $(this).toggleClass("checked");

        /* 测试--------------------- */
        console.log("当前name输入框的内容:", $("#name").val());
        console.log("当前address输入框的内容:", $("#address").val());



    });
    $("#reShot").on("click", function () {
        if (!$("#accept").hasClass("checked")) {
            $("#pic").addClass("hide");
            $("#takeVideo").removeClass("hide");
            showVideo(video);
        }
    });
});

/* 提交按钮 */
$(function () {
    $("#submit").on("click", function () {
        if ($("#pic>#accept").hasClass("checked") && $("#name").val() && $("#address").val()) {
            var data = {
                "name": $("#name").val(),
                "age": $("#age").val(),
                "phone": $("#phone").val(),
                "address": $("#address").val(),
                "person": $("#visitor").hasClass("checked") ? "visiters" : "owners",
                "image": $("#pic>img")[0].src,
            };
            $.ajax({
                url: "/personregister",
                data:JSON.stringify(data),
                type:"POST",
                contentType:"application/json;charset=utf-8",
                dataType:"json",
                success: function (respTest) {
                    console.log("返回的信息:", respTest);
                    if (respTest.status == 200) {
                        alert(respTest.data);
                        location.href = "/personregister";
                    }else if (respTest.statue == 201){
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
