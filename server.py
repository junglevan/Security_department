#coding=utf-8
import os
import time
import urllib
from datetime import timedelta
from flask import *
import base64
import re
from security_data import DatabaseModel
from check_car import car_check

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)

db = DatabaseModel()


@app.route("/")
def index_view():
    return render_template("index.html")
    #return 'hiya'

@app.route("/personregister", methods=["GET", "POST"])
def personregister_view():
    if request.method == "GET":
        return render_template("personregister.html")
    elif request.method == "POST":
        # print(request.get_json())
        name = request.get_json().get("name")
        age = request.get_json().get("age")
        phone = request.get_json().get("phone")
        address = request.get_json().get("address")
        # 人员性质,visiters:访客;owners:住户
        nature = request.get_json().get("person")
        data = request.get_json().get("image")
        # 提取图片信息
        result = re.search(r"^(?P<head>\w+):(?P<type>\w+)/(?P<file>\w+);(?P<codetype>[a-z0-9]+),(?P<content>.+$)",
                           data)
        # 转码
        details = base64.b64decode(result.group("content"))
        result = db.add_person(nature, name, phone, eval(address))
        print(result)
        try:
            ids = db.get_id(name, phone)
        except Exception as e:
            print("数据库id查找错误：", e)
        # 写入文件
        ids = str(ids)

        # 添加人员信息
        if not result:
            if not re.findall(r"1[0-9]{9}", phone):
                json_str = {"status": 201, "data": "手机号码输入有误"}
                return make_response(json.dumps(json_str))
            else:
                json_str = {"status": 203, "data": "地址输入或其他错误"}
                return make_response(json.dumps(json_str))

        else:
            # 测试代码
            # file = open("./static/imgs/compare/liudehua.jpg", "rb")
            # details = file.read(1024 * 1024)

            if nature == 'owners':
                with open("./static/imgs/sources/%s.png" % ids, "wb") as f:
                    f.write(details)
                    print("%s.png ok" % ids)

            json_str = {"status": 200, "data": "注册成功"}
            return make_response(json.dumps(json_str))


@app.route("/personcheck", methods=["GET", "POST"])
def personcheck_view():
    if request.method == "GET":
        return render_template("personcheck.html")
    elif request.method == "POST":
        recv = request.get_json()
        print(recv)
        data = request.get_json().get("image")
        result = re.search(r"^(?P<head>\w+):(?P<type>\w+)/(?P<file>\w+);(?P<codetype>[a-z0-9]+),(?P<content>.+$)",
                           data)
        details = data.split(",")[-1]
        print(result.group("content") == details)
        details = base64.b64decode(details)
        details = base64.b64decode(result.group("content"))
        filename = "check.png"
        with open("./static/imgs/compare/" + filename, "wb") as f:
            f.write(details)
        # 测试代码 代替前三行
        # filename = 'liudehua.jpg'
        compare_result = compare_pic(filename)
        result_check = db.check_person(compare_result, "in")
        # print("识别结果:", compare_result)
        if not compare_result or not result_check:
            status = 201
        else:
            status = 200

        return make_response(json.dumps({"status": status, "data": compare_result}))


# 人脸识别函数
def compare_pic(compare_filename):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
    key = "FgD_VV-Uitb0la4ZSJmvKGWy6322qgMP"
    secret = "FIkxoxnWI5bb3CC9nUMREkxck3X41_ri"
    filepath = "./static/imgs/compare/%s" % compare_filename  # 待对比文件路径
    # print("待对比文件相对路径:", filepath)
    fileList = []
    tempdir = []
    result = 0
    for root, dirs, files in os.walk("./static/imgs/sources/"):
        # print("root信息:", root)
        # print("dirs信息:", dirs)
        fileList = files  # 当前路径下所有非目录子文件名称
    # print("fileList信息:", fileList)
    for file in fileList:
        filepath2 = "./static/imgs/sources/%s" % file  # 需对比文件名称
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
        data.append(key)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
        data.append(secret)
        data.append('--%s' % boundary)
        fr = open(filepath, 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file1')
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr.read())
        fr.close()
        data.append('--%s' % boundary)
        fr2 = open(filepath2, 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file2')
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr2.read())
        fr2.close()
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
        data.append('1')
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
        data.append("gender,age,smiling,headpose,facequality,"
                    "blur,eyestatus,emotion,ethnicity,beauty,"
                    "mouthstatus,eyegaze,skinstatus")
        data.append('--%s--\r\n' % boundary)
        for i, d in enumerate(data):
            if isinstance(d, str):
                data[i] = d.encode('utf-8')

        http_body = b'\r\n'.join(data)
        # print(http_body)
        # build http request
        req = urllib.request.Request(url=http_url, data=http_body)

        # header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

        try:
            # post data to server
            resp = urllib.request.urlopen(req, timeout=50)
            # get response
            qrcont = resp.read()
            # if you want to load as json, you should decode first,
            # for example: json.loads(qrount.decode('utf-8'))
            # print(qrcont.decode('utf-8'))
            res = json.loads(qrcont.decode('utf-8'))
            # print("相似度:%s"%res.get("confidence"))
            # print("阈值：%s"%res.get("thresholds"))
            if res.get("confidence") and res.get("confidence") > 70:
                # result = "欢迎您：" + file
                result = file.split(".")[0]
                result = str(result)
                result = int(result)
                # result = True
                break
            # print(qrcont.decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(e.read().decode('utf-8'))
    # elapsed = (time.time() - start) #时间函数
    # print("Time used:", elapsed)    #程序运行时间
    return result


@app.route("/carregister", methods=["GET", "POST"])
def carregister_view():
    if request.method == "GET":
        return render_template("carregister.html")
    elif request.method == "POST":
        data = request.get_json()
        print("接受到的信息:", data)
        try:
            name = data.get("name")  # 姓名
            carId = data.get("carId")  # 车牌号
            phone = data.get("phone")  # 手机号
            address = data.get("address")  # 地址
            person = data.get("person")  # 人员性质
        except Exception as e:
            print("错误:", e)
            return make_response(json.dumps({"status": 201, "data": "数据有空"}))
        else:
            print(address)
            if not re.findall(r"[0-9]{10}", phone):
                return make_response(json.dumps({"status": 202, "data": "手机号格式有误"}))
            elif re.findall(r"\W+", carId):
                return make_response(json.dumps({"status": 203, "data": "车牌格式有误"}))
            if db.add_car(person, carId, eval(address), phone):
                return make_response(json.dumps({"status": 200, "data": "恭喜! 注册成功"}))
            else:
                return make_response(json.dumps({"status": 204, "data": "注册失败"}))


@app.route("/carcheck", methods=["GET", "POST"])
def carcheck_view():
    if request.method == "GET":
        return render_template("carcheck.html")
    elif request.method == "POST":
        print(request.get_json())
        data = request.get_json()
        # in:进;out:出
        dir = data.get("dir")
        # 车辆照片的文件名
        filename = data.get("filename")
        # 根据图片获取车牌信息
        result = car_check(filename)
        # 查询车辆是否有注册
        print(result)
        print("dir....................."+dir)
        re_car = db.check_car(result, dir)
        print(re_car)

        if re_car and dir == "in":
            json_str = {"status": 200, "data": "欢迎回家," + result}
            return make_response(json.dumps(json_str))
        elif re_car and dir == "out":
            json_str = {"status": 201, "data": "安全出行," + result}
            return make_response(json.dumps(json_str))
        elif (not re_car) and dir == "in":
            json_str = {"status": 202, "data": "无权进入,请先登记或重新加载图片"}
            return make_response(json.dumps(json_str))

        status = 200 if dir == "in" else 201
        return make_response(json.dumps({"status": status, "data": "OK"}))


@app.route("/aboutus")
def aboutus_view():
    return render_template("/aboutus.html")


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=7788,
            ssl_context=(
            #    "./static/server/server-cert.pem",
            #    "./static/server/server-key.pem",
                '/etc/nginx/cert/3649624_www.feidawebux.xyz.pem',
                '/etc/nginx/cert/3649624_www.feidawebux.xyz.key',
            )
            )
