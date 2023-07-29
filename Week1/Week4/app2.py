# https://www.cnblogs.com/feffery/p/16886578.html
from itsdangerous import URLSafeSerializer
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# 設定密鑰
app.secret_key = "密鑰可以是任何的字串，但是不要告訴別人"

# 建立一個加密器，使用 app 的密鑰作為參數
serializer = URLSafeSerializer(app.secret_key)


""" 首頁 """


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


""" 用來儲存註冊的帳號、密碼 """
users = {
    "user1": {"username": "user1", "password": "pass1"},
    "user2": {"username": "user2", "password": "pass2"}
}

""" 註冊 """


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username not in users:
            users[username] = {"username": username, "password": password}
            return render_template("register.html", message="恭喜，註冊成功！")
        else:
            message = "抱歉，帳號已經存在，請嘗試其他帳號。"
            return render_template("register.html", message="抱歉，帳號已經存在，請嘗試其他帳號。")
    return render_template("register.html", message=None)


""" 登入 """


@app.route("/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return redirect(url_for("error", message="帳號或密碼不得為空白"))
        if username in users and users[username]["password"] == password:
            # 登入成功後，將用戶名加密
            encrypted_username = serializer.dumps(username)

            response = redirect(url_for("member"))
            # 存儲在 cookie 中
            response.set_cookie("username", encrypted_username)
            return response
        else:
            return redirect(url_for("error", message="帳號或密碼輸入錯誤"))


""" 成功 """


@app.route("/member")
def member():
   # 從 cookie 中讀取加密後的用戶名，如果 cookie 被刪除，轉跳登入畫面
    encrypted_username = request.cookies.get("username")
    if not encrypted_username:
        return redirect(url_for("login"))

    try:
        # 解密用戶名
        username = serializer.loads(encrypted_username)
        return render_template("member.html", username=username)
    except:
        # 解密失敗，轉跳到登入頁面
        return redirect(url_for("login"))


""" 登出 """


@app.route("/signout", methods=["GET"])
def signout():
    # 清除 cookie 中的用戶名
    response = redirect(url_for("login"))
    response.delete_cookie("username")
    return response


""" 失敗 """


@app.route("/error")
def error():
    message = request.args.get("message")
    return render_template("error.html", message=message)


""" 計算 """


@app.route("/square/<int:number>", methods=["GET"])
def square(number):
    squared_number = number ** 2
    return render_template("square.html", squared_number=squared_number)


""" 啟動 """
app.run(port=3000)
