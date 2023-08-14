from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify  # 將 Python 的資料結構轉換為 JSON 格式
import mysql.connector.pooling

app = Flask(__name__)
app.secret_key = "密鑰可以是任何的字串，但是不要告訴別人"


db = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "website",
    "pool_size": 8
}


connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db)

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
    if signup_check(connection_pool, username) is None:
        signup_new_user(connection_pool, name, username, password)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("error", message="帳號已經被註冊"))


""" 檢查帳號是否註冊過 """


def signup_check(connection_pool, username):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))
    data = cur.fetchone()
    cur.close()
    connection.close()
    return data


""" 新註冊姓名、帳號、密碼 """


def signup_new_user(connection_pool, name, username, password):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    cur.execute(sql, (name, username, password))
    connection.commit()
    cur.close()
    connection.close()


""" 登入 """


@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if signin_check(connection_pool, username, password) is None:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))
    else:
        session["signin_username"] = username
        return redirect(url_for("member"))


""" 檢查帳號密碼是否正確 """


def signin_check(connection_pool, username, password):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "SELECT * FROM member WHERE username = %s AND password = %s"
    cur.execute(sql, (username, password))
    data = cur.fetchone()
    cur.close()
    connection.close()
    return data


""" 會員頁面 """


@app.route("/member")
def member():
    member_username = session.get("signin_username")
    if member_username:
        member_data = user_data(connection_pool, member_username)
        """ 取得留言板功能需要的相關資訊 """
        messages_data = get_messages(connection_pool)
        return render_template("member.html", member_data=member_data, messages=messages_data)
    return redirect(url_for("login"))


""" 依據登入的帳號，找出該會員的相關資訊 """


def user_data(connection_pool, username):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    cur.execute(sql, (username,))
    data = cur.fetchone()
    cur.close()
    connection.close()
    return data


""" 找出留言人的姓名以及內容，並且依時間小到大排序 """
""" 找出帳號以及message.id，連接刪除留言的功能 """


def get_messages(connection_pool):
    connection = connection_pool.get_connection()
    cur = connection.cursor(dictionary=True)
    sql = "SELECT member.username,member.name, message.id,message.content FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
    cur.execute(sql)
    messages = cur.fetchall()
    cur.close()
    connection.close()
    return messages


""" 留言板 """


@app.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form["content"]
    username = session.get("signin_username")
    """ 依據登入的帳號，找出該會員的相關資訊 """
    member_data = user_data(connection_pool, username)
    member_id = member_data[0]
    """ 依據member_id，新增留言 """
    save_message(connection_pool, member_id, content)
    return redirect(url_for("member"))


""" 新增member_id、留言內容 """


def save_message(connection_pool, member_id, content):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    cur.execute(sql, (member_id, content))
    connection.commit()
    cur.close()
    connection.close()


""" 刪除留言 """


@app.route("/deleteMessage", methods=["POST"])
def delete_message():
    """ 回傳點擊的留言id(index) """
    message_id = request.form["message_id"]
    """ 刪除特定留言 """
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "DELETE FROM message WHERE id = %s"
    cur.execute(sql, (message_id,))
    connection.commit()
    cur.close()
    connection.close()
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


# -----------------新增查詢會員資料功能、修改會員姓名功能-------------


""" 查詢會員資料 """
# https://cloud.tencent.com/developer/article/2086436


@app.route('/api/member')
def api_get_member():
    username = request.args.get('username')  # 從JS要求的URL的要求字串取得 username
    member_data = get_member_by_username(connection_pool, username)
    if member_data:
        response = {'data': member_data}
    else:
        response = {'data': None}  # Python的None對應JSON格式為null

    return jsonify(response)  # 轉換為JSON格式（如果為字典時，Flask背後也會處理JSON格式，所以其實也可以不用加）


""" 透過會員帳號，查詢id、name、username """


def get_member_by_username(connection_pool, username):
    connection = connection_pool.get_connection()
    cur = connection.cursor(dictionary=True)
    sql = "SELECT id, name, username FROM member WHERE username = %s"
    cur.execute(sql, (username,))
    data = cur.fetchone()
    cur.close()
    connection.close()
    return data

# http://127.0.0.1:3000/api/member?username=111 測試成功


""" 修改會員姓名 """


@app.route('/api/member', methods=['PATCH'])
def api_update_member_name():
    # 根據session狀態檢查如果不是登入的會員，不能更改姓名
    if 'signin_username' not in session:
        response = {'error': True}
    else:
        new_name = request.json.get('name')
        if new_name:
            update_result = update_member_name(
                connection_pool, session['signin_username'], new_name)
            if update_result:
                response = {'ok': True, "newName": new_name}
            else:
                response = {'error': True}
        else:
            response = {'error': True}

    return jsonify(response)


def update_member_name(connection_pool, username, new_name):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "UPDATE member SET name = %s WHERE username = %s"
    cur.execute(sql, (new_name, username))
    connection.commit()
    cur.close()
    connection.close()
    return True  # True 表示更新成功


""" 啟動 """
app.run(port=3000)
