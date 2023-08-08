""" 安裝套件 pip install mysql-connector-python """
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "密鑰可以是任何的字串，但是不要告訴別人"

""" 連線到資料庫 """
mydb = mysql.connector.connect(
    user="root",
    password="123456",
    host="localhost",
    database="website"
)

""" 首頁 """


@app.route("/")
def login():
    return render_template("login.html")


""" 註冊 """


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form['name']
    username = request.form["username"]
    password = request.form["password"]
    if signup_check(username):
        return redirect(url_for("error", message="帳號已經被註冊"))
    else:
        """ 增加新註冊的姓名、帳號、密碼 """
        cur = mydb.cursor()
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        cur.execute(sql, (name, username, password))
        mydb.commit()  # 確定新增資料
        cur.close()
        return redirect(url_for("login"))


""" 檢查帳號是否註冊過 """


def signup_check(username):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))  # 執行SQL語法，注意","就算只有一個也要加",""
    data = cur.fetchone()  # 取得一筆資料
    cur.close()
    return data is not None  # 若data不為空值(代表有被註冊過)，顯示T


""" 登入 """


@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if signin_check(username, password):
        session["username"] = username
        return redirect(url_for("member"))
    else:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))


""" 檢查帳號密碼是否正確 """


def signin_check(username, password):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s AND password = %s"
    cur.execute(sql, (username, password))
    data = cur.fetchone()
    cur.close()
    return data is not None


""" 會員頁面 """


@app.route("/member")
def member():
    member_username = session.get("username")
    if member_username:
        """ 依據登入的帳號找出使用者名稱 """
        member_data = user_data(member_username)
        member_name = member_data[1]
        """ 取得留言姓名、內容 """
        messages = get_messages()
        return render_template("member.html", name=member_name, messages=messages)
    return redirect(url_for("login"))


""" 找出登入的帳號 """


def user_data(username):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))
    data = cur.fetchone()
    cur.close()
    return data


""" 找出留言人的姓名以及內容，並且依時間小到大排序 """


def get_messages():
    cur = mydb.cursor(dictionary=True)
    sql = "SELECT member.name, message.content FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
    cur.execute(sql)
    messages = cur.fetchall()  # 取得多筆資料
    cur.close()
    return (messages)


""" 留言板 """


@app.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form["content"]
    username = session.get("username")
    if username:
        """ 依登入的帳號，找出對應的member_id """
        member_data = user_data(username)
        member_id = member_data[0]
        """ 依據member_id，新增留言 """
        save_message(member_id, content)
        return redirect(url_for("member"))
    else:
        return redirect(url_for("login"))


""" 新增member_id、留言內容 """


def save_message(member_id, content):
    cur = mydb.cursor()
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    cur.execute(sql, (member_id, content))
    mydb.commit()
    cur.close()


""" 登出 """


@app.route("/signout")
def signout():
    session.pop("username", None)
    return redirect(url_for("login"))


""" 錯誤 """


@app.route("/error")
def error():
    message = request.args.get("message")
    return render_template("error.html", message=message)


""" 啟動 """
app.run(port=3000)
