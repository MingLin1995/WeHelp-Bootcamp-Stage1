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
    if signup_check(username) is None:
        signup_new_user(name, username, password)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("error", message="帳號已經被註冊"))


""" 檢查帳號是否註冊過 """


def signup_check(username):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))  # 執行SQL語法，注意","就算只有一個也要加",""
    data = cur.fetchone()  # 取得一筆資料
    cur.close()
    print(data)
    return data


""" 新註冊姓名、帳號、密碼 """


def signup_new_user(name, username, password):
    cur = mydb.cursor()
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    cur.execute(sql, (name, username, password))
    mydb.commit()  # 確定新增資料
    cur.close()


""" 登入 """


@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if signin_check(username, password) is None:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))
    else:
        session["signin_username"] = username
        return redirect(url_for("member"))


""" 檢查帳號密碼是否正確 """


def signin_check(username, password):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s AND password = %s"
    cur.execute(sql, (username, password))
    data = cur.fetchone()
    cur.close()
    return data


""" 會員頁面 """


@app.route("/member")
def member():
    member_username = session.get("signin_username")
    if member_username:
        member_data = user_data(member_username)
        """ 取得留言板功能需要的相關資訊 """
        messages_data = get_messages()
        return render_template("member.html", member_data=member_data, messages=messages_data)
    return redirect(url_for("login"))


""" 依據登入的帳號，找出該會員的相關資訊 """


def user_data(username):
    cur = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))
    data = cur.fetchone()
    cur.close()
    return data


""" 找出留言人的姓名以及內容，並且依時間小到大排序 """
""" 找出帳號以及message.id，連接刪除留言的功能 """


def get_messages():
    cur = mydb.cursor(dictionary=True)
    sql = "SELECT member.username,member.name, message.id,message.content FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
    cur.execute(sql)
    messages = cur.fetchall()
    cur.close()
    return messages


""" 留言板 """


@app.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form["content"]
    username = session.get("signin_username")
    """ 依據登入的帳號，找出該會員的相關資訊 """
    member_data = user_data(username)
    member_id = member_data[0]
    """ 依據member_id，新增留言 """
    save_message(member_id, content)
    return redirect(url_for("member"))


""" 新增member_id、留言內容 """


def save_message(member_id, content):
    cur = mydb.cursor()
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    cur.execute(sql, (member_id, content))
    mydb.commit()
    cur.close()


""" 刪除留言 """


@app.route("/deleteMessage", methods=["POST"])
def delete_message():
    """ 回傳點擊的留言id(index) """
    message_id = request.form["message_id"]
    """ 刪除特定留言 """
    cur = mydb.cursor()
    sql = "DELETE FROM message WHERE id = %s"
    cur.execute(sql, (message_id,))
    mydb.commit()
    cur.close()
    return redirect(url_for("member"))


""" 登出 """


@app.route("/signout")
def signout():
    session.pop("signin_username")
    return redirect(url_for("login"))


""" 錯誤 """


@app.route("/error")
def error():
    message_error = request.args.get("message")
    return render_template("error.html", msg=message_error)


""" 啟動 """
app.run(port=3000)
