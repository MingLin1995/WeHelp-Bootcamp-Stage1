""" https://ithelp.ithome.com.tw/articles/10258223 關鍵字：網頁模版與資料接口"""
""" session 參考教學#12"""
# 建立樣本檔案，放在在專案的templates資料夾底下
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
# 靜態檔案處理 folder指定資料夾名稱 預設為static

""" session載入背後加密機制 """
app.secret_key = "密鑰可以是任何的字串，但是不要告訴別人"


""" 首頁 """


@app.route("/", methods=["GET", "POST"])  # methods 預設GET
def login():
    return render_template("login.html")  # 將HTML模板給使用者的伺服器


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
            # render_template()第二個參數可以附帶資料內容傳送到前端，HTML透過{{ }}就可以顯示出來
            return render_template("register.html", message="恭喜，註冊成功！")
        else:
            message = "抱歉，帳號已經存在，請嘗試其他帳號。"
            # 註冊失敗，顯示錯誤訊息
            return render_template("register.html", message="抱歉，帳號已經存在，請嘗試其他帳號。")

    return render_template("register.html", message=None)  # 第一次請求時，不顯示任何訊息


""" 登入 """


@app.route("/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # 檢查是否有輸入帳號密碼
        if not username or not password:
            # 網頁重新導向，並且添加要求字串
            return redirect(url_for("error", message="帳號或密碼不得為空白"))

        # 進行登入驗證
        if username in users and users[username]["password"] == password:
            # 登入成功後，將用戶名存儲在session中
            session["username"] = username
            return redirect(url_for("member"))  # 登入成功，轉跳到/member頁面
        else:
            # 登入失敗，轉跳到/error頁面
            return redirect(url_for("error", message="帳號或密碼輸入錯誤"))


""" 成功 """


@app.route("/member")
def member():
    # 如果 "username"的鍵存在，就會返回對應的值，否則的話返回None
    if session.get("username", None):
        return render_template("member.html")
    return redirect(url_for("login"))


""" 登出 """


@app.route("/signout", methods=["GET"])
def signout():
    # https://ithelp.ithome.com.tw/articles/10268922
    # 清除session中的用戶名(鍵)
    session.pop("username", None)
    return redirect(url_for("login"))


""" 失敗 """


@app.route("/error")
def error():
    # 從URL查詢字串中，獲取message
    message = request.args.get("message")
    return render_template("error.html", message=message)


""" 計算 """


@app.route("/square/<int:number>", methods=["GET"])
# 註冊路由除了固定的導向位址，URL 也可以成為函式接收的參數
def square(number):
    squared_number = number ** 2
    return render_template("square.html", squared_number=squared_number)


""" 啟動 """
app.run(port=3000)
