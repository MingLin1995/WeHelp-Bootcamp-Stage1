from flask import Flask, jsonify, request
# from flask_cors import CORS

app = Flask(__name__)
# 啟用CORS
# CORS(app)

# 第一種方法，透過Flask套件，會自動設置CORS所需資訊。


@app.route("/", methods=["GET"])
def api():
    response = {"message": "連接成功"}
    return jsonify(response)


# 第二種方法，自己設定 Access-Control-Allow-Origin
""" 
1.瀏覽器發送跨域請求，伺服器回傳回來標頭特別是Origin，瀏覽器確認允許跨域請求。（若不允許就會跳出CORS錯誤）
2.發送實際請求前，會先發送預檢請求OPTIONS，如果預檢請求成功，瀏覽器才會發送真正的請求GET
"""


@app.route("/", methods=["OPTIONS", "GET"])
def api():
    if request.method == "OPTIONS":
        # 預檢請求
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    else:
       # 實際請求
        response = jsonify({"message": "連接成功"})
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"

    return response


if __name__ == "__main__":
    app.run()
