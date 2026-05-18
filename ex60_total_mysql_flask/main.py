from flask import Flask, render_template, request, jsonify, session, url_for, redirect

from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os

# env 파일을 관리하는 이유는 보안상의 이유로 민감한 정보를 코드에 직접 작성하지 않기 위해서입니다. github에 코드를 올릴 때 gitignore에 env 파일을 추가하여 민감한 정보가 공개되지 않도록 합니다.
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# MYSQL_HOST=localhost
# MYSQL_USER=root
# MYSQL_PASSW   ORD=1234
# MYSQL_DB=bookstore_flask
# 지금은 학습중이니 작성했지만 실제로는 민감정보는 주석으로도 작성금지 env 파일로 관리하기

# crud        /sql  /web(restful api)
# c: create : insert/POST
# r: read : select  /GET ex) 브라우저 주소창 입력
# u: update : update/PUT(한 줄 전체 교환) or PATCH(일부 교환)
# d: delete : delete/delete

app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 
mysql = MySQL(app)

def is_logged_in():# 로그인 여부를 확인하는 함수입니다. session에 'logged_in'이 있는지 확인하여 로그인 여부를 판단합니다. 로그인한 사용자의 정보를 session에 저장하기 때문에 session에 'logged_in'이 있으면 로그인한 상태로 간주합니다.
    return 'logged_in' in session

@app.route('/') #로그인이 되어있으면 책 목록 페이지로 리다이렉트하고, 로그인되어 있지 않으면 로그인 페이지를 렌더링하는 라우트입니다.
def index(): # 로그인 페이지로 이동하는 라우트입니다. 로그인되어 있으면 책 목록 페이지로 리다이렉트하고, 로그인되어 있지 않으면 로그인 페이지를 렌더링합니다.
    if is_logged_in(): return # redirect(url_for('books_page')) # 로그인되어 있으면 책 목록 페이지로 리다이렉트합니다.
    return render_template('login.html') # 로그인되어 있지 않으면 로그인 페이지를 렌더링합니다. 
        
@app.route('/register_page')# 회원 가입 페이지로 이동하는 라우트입니다. 
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customer (name, address, phone, password) VALUES (%s, %s, %s, %s)", (data['name'], data['address'], data['phone'], hashed_pw))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True, 'message': '회원 가입 잘 되었음'})

@app.route('/api/login', methods=['POST']) 
def api_login():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer WHERE name = %s", (data['name'],))
    user = cur.fetchone()
    cur.close()
    if user and check_password_hash(user['password'], data['password']):
        session['logged_in'] = True
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return jsonify({'success': True, 'message': '로그인 성공'})
    return jsonify({'success': False, 'message': 'ID 또는 비밀번호가 잘못되었습니다.'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)



































































































    