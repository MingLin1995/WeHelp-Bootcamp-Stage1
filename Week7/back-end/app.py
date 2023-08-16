from flask import Flask, request, session
from flask import jsonify  # 將 Python 的資料結構轉換為 JSON 格式
import mysql.connector.pooling
# pip install flask-cors
from flask_cors import CORS  # 處理跨域問題
#pip install pyjwt
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "密鑰可以是任何的字串，但是不要告訴別人"


CORS(app)  # 允许所有源的请求

db = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "website",
    "pool_size": 8
}


connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db)

""" 首頁 """


""" @app.route("/")
def login():
    return jsonify({"type":"success","message": "working now"}) """


""" 註冊 """


@app.route("/member/signup", methods=["POST"])
def signup():
    data = request.json  # 前端以 JSON 格式提交數據
    name = data['name']
    username = data["username"]
    password = data["password"]
    if signup_check(connection_pool, username) is None:
        signup_new_user(connection_pool, name, username, password)
        return jsonify({"type":"success","message": "註冊成功"})
    else:
        return jsonify({"type":"error","message": "帳號已經被註冊"})


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


@app.route("/member/signin", methods=["POST"])
def signin():
    data = request.json
    username = data["username"]
    password = data["password"]
    if signin_check(connection_pool, username, password) is None:
        return jsonify({"type":"error","message": "帳號或密碼輸入錯誤"})
    else:
        signin_check(connection_pool, username, password)

        # 生成 JWT
        payload = {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({"type":"success","message": "登入成功","username":username,"token":token})


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

""" 驗證token """
@app.route("/member/verify_token", methods=["POST"])
def verify_token():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401
    try:
        decoded_token = jwt.decode(token.split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        # 在這裡可以檢查其他 token 的內容，確認用戶的身份等等
        return jsonify({"message": "Token is valid", "username": decoded_token.get("username")}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

""" 會員頁面 """


@app.route("/member/get_name", methods=["POST"])
def get_name():
    data = request.json
    """ 依據帳號，找出會員資訊 """
    username = data["username"]
    member_data = user_data(connection_pool, username)
    member_name=member_data[1]
    return jsonify({"type":"success","message": "登入成功","memberName":member_name})




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

""" 留言板 """
@app.route("/message/get_content", methods=["POST"])
def get_content():
    """ 取得留言板功能需要的相關資訊 """
    messages_data = get_messages(connection_pool)
    return jsonify({"type":"success","messagesData":messages_data})

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


@app.route("/message/create_message", methods=["POST"])
def create_message():
    """ 依據登入的帳號，新增留言內容 """
    data = request.json
    username = data["username"]
    content=data["content"]
    """ 依據登入的帳號，找出該會員的id """
    member_data = user_data(connection_pool, username)
    member_id = member_data[0]

    """ 依據member_id，新增留言 """
    save_message(connection_pool, member_id, content)
    return jsonify ({"type":"success"})


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
@app.route("/message/delete/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    # 解析 JWT，獲取使用者資訊
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded_token = jwt.decode(token.split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token.get("username")
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    # 比較留言的擁有者與目前登入的使用者名稱
    if is_message_owner(connection_pool, message_id, username):
        # 執行刪除留言的動作，這裡假設你有一個名為 delete_message_by_id 的函式
        success = delete_message_by_id(connection_pool, message_id)
        print(success)

        if success:
            return jsonify({"type": "success", "message": "留言刪除成功"})
        else:
            return jsonify({"type": "error", "message": "無法刪除留言"})
    else:
        return jsonify({"type": "error", "message": "無權限刪除該留言"})

def is_message_owner(connection_pool, message_id, username):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "SELECT member.username FROM message INNER JOIN member ON message.member_id = member.id WHERE message.id = %s"
    cur.execute(sql, (message_id,))
    result = cur.fetchone()
    cur.close()
    connection.close()

    if result and result[0] == username:
        return True
    else:
        return False

def delete_message_by_id(connection_pool, message_id):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    sql = "DELETE FROM message WHERE id = %s"
    cur.execute(sql, (message_id,))
    connection.commit()
    cur.close()
    connection.close()
    return "ok"



""" 登出 """


""" @app.route("/signout")
def signout():
    session.pop("signin_username")
    return redirect(url_for("login")) """


""" 錯誤 """


""" @app.route("/member/error")
def error():
    return jsonify({"type":"success","message": "帳號已經被註冊"}) """


# -----------------新增查詢會員資料功能、修改會員姓名功能-------------

""" 查詢會員資料 """
# https://cloud.tencent.com/developer/article/2086436


@app.route('/member/get_username')
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


@app.route('/member/update_name', methods=['PATCH'])
def api_update_member_name():
    data = request.json
    """ 依據帳號，找出會員資訊 """
    username = data["username"]
    new_name = data["newName"]
    update_member_name(connection_pool, username, new_name)
    return jsonify({"ok": True, "newName": new_name})

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
app.run(port=5000)
