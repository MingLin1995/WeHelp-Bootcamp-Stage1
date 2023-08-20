from flask import Flask, request
from flask import jsonify  # 將 Python 的資料結構轉換為 JSON 格式
import mysql.connector.pooling
# pip install flask-cors
from flask_cors import CORS  # 處理跨域問題
# pip install pyjwt
import jwt
import time
# https://ithelp.ithome.com.tw/m/articles/10269768
# https://geek-docs.com/python/python-tutorial/j_python-jwt.html

app = Flask(__name__)
CORS(app)  # 啟用CORS

header = {
    "alg": "HS256",  # 簽名技術
    "typ": "JWT"  # 類型
}

app.config['SECRET_KEY'] = "密鑰可以是任何的字串，但是不要告訴別人"


db = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "website",
    "pool_size": 8
}


connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db)

""" 註冊 """


@app.route("/member/signup", methods=["POST"])
def signup():
    data = request.json  # 前端以 JSON 格式提交數據
    name = data["name"]
    username = data["username"]
    password = data["password"]
    if signup_check(connection_pool, username) is None:
        signup_new_user(connection_pool, name, username, password)
        return jsonify({"type": "success", "message": "註冊成功"})
    else:
        return jsonify({"type": "fail", "message": "帳號已經被註冊"})


""" 檢查帳號是否註冊過 """


def signup_check(connection_pool, username):
    sql = "SELECT * FROM member WHERE username = %s"
    return execute_query(connection_pool, sql, (username,), fetch_one=True)


""" 新註冊姓名、帳號、密碼 """


def signup_new_user(connection_pool, name, username, password):
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    execute_query(connection_pool, sql,
                  (name, username, password), commit=True)


""" 登入 """


@app.route("/member/signin", methods=["POST"])
def signin():
    data = request.json
    username = data["username"]
    password = data["password"]
    if signin_check(connection_pool, username, password) is None:
        return jsonify({"type": "fail", "message": "帳號或密碼輸入錯誤"})
    else:
        signin_check(connection_pool, username, password)

        # 建立token
        payload = {'username': username,
                   'exp': time.time() + 60*60}
        token = jwt.encode(
            payload, app.config['SECRET_KEY'], algorithm="S256", headers=header)
        # 將新建立的token存入資料庫
        save_token(connection_pool, username, token)
        return jsonify({"type": "success", "message": "登入成功", "username": username, "token": token})


""" 檢查帳號密碼是否正確 """


def signin_check(connection_pool, username, password):
    sql = "SELECT * FROM member WHERE username = %s AND password = %s"
    return execute_query(connection_pool, sql, (username, password), fetch_one=True)


""" 將token存入資料庫 """


def save_token(connection_pool, username, token):
    connection = connection_pool.get_connection()
    cur = connection.cursor()

    # 找到對應的 member_id
    find_member_id_sql = "SELECT id FROM member WHERE username = %s"
    cur.execute(find_member_id_sql, (username,))
    member_id = cur.fetchone()

    # 檢查是否已存在該 member_id 的 token 記錄
    find_token_sql = "SELECT member_id FROM token WHERE member_id = %s"
    cur.execute(find_token_sql, (member_id[0],))
    old_token_id = cur.fetchone()

    # 如果有 token 刪除舊的 token 記錄
    if old_token_id:
        delete_token_sql = "DELETE FROM token WHERE member_id = %s"
        cur.execute(delete_token_sql, (old_token_id[0],))

    # 如果沒有 token ，則新增 token到資料庫
    insert_token_sql = "INSERT INTO token (member_id, token) VALUES (%s, %s)"
    cur.execute(insert_token_sql, (member_id[0], token))
    connection.commit()

    cur.close()
    connection.close()


""" ---------------------------Token檢查--------------------------- """
""" 驗證token """


@app.route("/member/verify_token", methods=["POST"])
def verify_token():
    # 取的前端傳過來的token、帳號
    token = request.headers.get("Authorization")
    username = request.headers.get("username")
    # print(token)
    token = token.replace("Bearer ", "")
    # 如果為空值
    if not token:
        return jsonify({"type": "fail", "message": "沒有Token"})

    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=["HS256"])
        # 驗證帳號是否一致
        if decoded_token.get("username") == username:
            # 驗證 token 是否與資料庫中的一致
            if check_token(connection_pool, token):
                return jsonify({"type": "success", "message": "核對成功"})
            else:
                return jsonify({"type": "fail", "message": "核對失敗"})
        else:
            return jsonify({"type": "fail", "message": "核對失敗"})
    except jwt.ExpiredSignatureError:
        return jsonify({"type": "fail", "message": "Token過期"})
    except jwt.DecodeError:
        return jsonify({"type": "fail", "message": "Token解碼失敗"})


def check_token(connection_pool, token):
    sql = "SELECT * FROM token WHERE token = %s"
    return execute_query(connection_pool, sql, (token,), fetch_one=True)


""" 登出 """


@app.route("/member/logout", methods=["DELETE"])
def logout():
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")
    if delete_token(connection_pool, token):
        return jsonify({"type": "success", "message": "登出成功"})
    else:
        return jsonify({"type": "error", "message": "登出失敗"})


def delete_token(connection_pool, token):
    try:
        # 先解除刪除的安全機制
        sql_1 = "set sql_safe_updates=0"
        execute_query(connection_pool, sql_1, commit=True)

        # 執行刪除
        sql_2 = "DELETE FROM token WHERE token = %s"
        execute_query(connection_pool, sql_2, (token,), commit=True)

        # 恢復安全機制
        sql_3 = "set sql_safe_updates=1"
        execute_query(connection_pool, sql_3, commit=True)

        return True
    except Exception as e:
        print("刪除 token 時發生錯誤:", str(e))
        return False


""" 會員頁面 """


@app.route("/member/get_name", methods=["GET"])
def get_name():
    username = request.args.get("username")  # 直接取得使用者名稱字串
    """ 依據帳號，找出會員資訊 """
    member_data = user_data(connection_pool, username)
    member_name = member_data[1]
    return jsonify({"type": "success", "message": "登入成功", "memberName": member_name})


""" 依據登入的帳號，找出該會員的相關資訊 """


def user_data(connection_pool, username):
    sql = "SELECT * FROM member WHERE username = %s"
    return execute_query(connection_pool, sql, (username,), fetch_one=True)


""" ------------------查詢帳號、更新姓名功能------------------- """
""" 查詢會員資料 """


@app.route('/member/get_username')
def api_get_member():
    username = request.args.get("username")
    member_data = get_member_by_username(connection_pool, username)
    if member_data:
        response = {"type": "success", "message": member_data}
    else:
        response = {"type": "fail", "message": "查無此會員或帳號輸入錯誤"}
    return jsonify(response)


""" 透過會員帳號，查詢id、name、username """


def get_member_by_username(connection_pool, username):
    sql = "SELECT id, name, username FROM member WHERE username = %s"
    return execute_query(connection_pool, sql, (username,), fetch_one=True)

# http://127.0.0.1:3000/api/member?username=111 測試成功


""" 更新會員姓名 """


@app.route('/member/update_name', methods=['PATCH'])
def api_update_member_name():
    data = request.json
    """ 依據帳號，找出會員資訊 """
    username = data["username"]
    new_name = data["newName"]
    update_member_name(connection_pool, username, new_name)
    return jsonify({"type": "success", "message": new_name})


def update_member_name(connection_pool, username, new_name):
    sql = "UPDATE member SET name = %s WHERE username = %s"
    execute_query(connection_pool, sql, (new_name, username), commit=True)
    return "ok"


""" ---------------------------留言板功能--------------------------- """
""" 留言板 """


@app.route("/message/get_content", methods=["POST"])
def get_content():
    """ 取得留言板功能需要的相關資訊 """
    messages_data = get_messages(connection_pool)
    return jsonify({"type": "success", "messagesData": messages_data})


""" 找出留言人的姓名以及內容，並且依時間小到大排序 """
""" 找出帳號以及message.id，連接刪除留言的功能 """


def get_messages(connection_pool):
    sql = "SELECT member.username, member.name, message.id, message.content FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC"
    return execute_query(connection_pool, sql, fetch_one=False)


""" 留言功能 """


@app.route("/message/create_message", methods=["POST"])
def create_message():
    """ 依據登入的帳號，新增留言內容 """
    data = request.json
    print(data)
    username = data["username"]
    content = data["content"]
    """ 依據登入的帳號，找出該會員的id """
    member_data = user_data(connection_pool, username)
    member_id = member_data[0]
    """ 依據member_id，新增留言 """
    save_message(connection_pool, member_id, content)
    return jsonify({"type": "success"})


""" 新增member_id、留言內容 """


def save_message(connection_pool, member_id, content):
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    execute_query(connection_pool, sql, (member_id, content), commit=True)


""" 刪除留言 """


@app.route("/message/delete/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    # 透過message_id 找出使用者帳號
    username = is_message_owner(connection_pool, message_id)[0]

    # 判斷token的帳號是否與刪除的帳號一致
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")

    if not token:
        return jsonify({"type": "fail", "message": "沒有Token"})
    try:
        # 解碼token
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=["HS256"])
        # 驗證帳號是否一致
        if decoded_token.get("username") == username:
            # 刪除留言
            delete_message_by_id(connection_pool, message_id)
            return jsonify({"type": "success", "message": "刪除成功"})
        else:
            return jsonify({"type": "fail", "message": "刪除失敗"})
    # 如果過期
    except jwt.ExpiredSignatureError:
        return jsonify({"type": "fail", "message": "Token過期"})


def is_message_owner(connection_pool, message_id):
    sql = "SELECT member.username FROM message JOIN member ON message.member_id = member.id WHERE message.id = %s"
    return execute_query(connection_pool, sql, (message_id,), fetch_one=True)


def delete_message_by_id(connection_pool, message_id):
    sql = "DELETE FROM message WHERE id = %s"
    execute_query(connection_pool, sql, (message_id,), commit=True)
    return "ok"


""" ---------------------簡化資料庫溝通流程------------------------ """


def execute_query(connection_pool, sql, params=None, fetch_one=False, commit=False):
    connection = connection_pool.get_connection()
    cur = connection.cursor()
    cur.execute(sql, params)

    if fetch_one:
        data = cur.fetchone()
    else:
        data = cur.fetchall()

    if commit:
        connection.commit()

    cur.close()
    connection.close()

    return data


""" 啟動 """
app.run(port=5000)
