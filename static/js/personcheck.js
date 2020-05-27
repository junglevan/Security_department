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
            if ("srcObject" in video) {
                camareStream = stream;
                video.srcObject = stream;
            }else{
                var url = window.URL || window.webkitURL;
                video.src = url ? url.createObjectURL(stream) : stream;
            }
            video.addEventListener("canplay", function (ev) {
                if (stream.active) {
                    video.play();
                }
            }, false);
        }

        function error(err) {
            console.log("错误：", err);
        }

        if (navigator.getUserMedia) {
            navigator.getUserMedia(config,success, error); 
        }else{
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
    $("#accept").on("click", function () {
        var data = {
            "image": $("#pic>img")[0].src,
        };
        $.ajax({
            url: "/personcheck",
            data:JSON.stringify(data),
            type:"POST",
            contentType:"application/json;charset=utf-8",
            dataType:"json",
            success: function (respTest) {
                if (respTest.status == 200) {
                    $("#feedback").removeClass("hide").siblings().addClass("hide");
                    // alert(respTest.data);
                    setTimeout(function () {
                        location.href = "/personcheck";
                    },2000);
                }else{
                    if(confirm("未识别到或未登记,是否重新识别?")){
                        location.href = "/personcheck";
                    }else{
                        location.href = "/personregister";
                    }
                }
            },
            error: function (err) {
                console.log(err);
            }
        });

        // $("#final").addClass("hide");
        // $("#loading").removeClass("hide");

    });
});
