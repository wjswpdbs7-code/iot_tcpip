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
    if is_logged_in(): return redirect(url_for('books_page')) # 로그인되어 있으면 책 목록 페이지로 리다이렉트합니다.
    return render_template('login.html') # 로그인되어 있지 않으면 로그인 페이지를 렌더링합니다. 
        
@app.route('/register_page')# 회원 가입 페이지로 이동하는 라우트입니다. 
def register_page():
    return render_template('register.html')

@app.route('/books') 
def books_page():
    if not is_logged_in(): return redirect(url_for('index'))
    return render_template('books.html')

@app.route('/add_book', methods=['POST']) 
def add_book():
    if not is_logged_in(): return redirect(url_for('index'))
    return render_template('add_book.html')


@app.route('/api/books', methods=['GET'])
def api_get_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM book")
    books = cur.fetchall()
    cur.close()
    return jsonify(books)

@app.route('/api/add_book', methods=['POST'])
def api_add_book():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO book (bookname, publisher, price) VALUES (%s, %s, %s)", (data['bookname'], data['publisher'], data['price']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/api/order', methods=['POST'])
def api_order():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (custid, bookid, saleprice, order_date) \
                VALUES (%s, %s, %s, %s)", (session['custid'], data['bookid'], data['price'], datetime.now())
                )
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/my_orders')
def my_order_page():
    if not is_logged_in(): return redirect(url_for('index')) # 로그인이 안되있으면 로그인 페이지로 리다이렉트합니다.
    return render_template('my_orders.html')

@app.route('/api/my_orders', methods=['GET'])
def api_get_my_orders():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT o.orderid, o.orderdate, o.saleprice, b.bookname 
                FROM orders o JOIN book b 
                ON o.bookid = b.id 
                WHERE o.custid =%s
                """, (session['custid']))
    
    orders = cur.fetchall()
    cur.close()
    return jsonify(orders)

@app.route('/logout')  
def logout(): 
    session.clear()
    return redirect(url_for('index'))

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
        session['user_id'] = user['custid'] 
        session['user_name'] = user['name']
        return jsonify({'success': True, 'message': '로그인 성공'})
    return jsonify({'success': False, 'message': 'ID 또는 비밀번호가 잘못되었습니다.'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)


# @app.route란 Flask에서 라우트를 정의하는 데코레이터입니다. 라우트는 웹 애플리케이션에서 특정 URL 경로에 대한 요청을 처리하는 함수를 연결하는 역할을 합니다. 
#예를 들어, @app.route('/api/login', methods=['POST'])는 '/api/login' 경로에 대한 POST 요청이 들어왔을 때 api_login 함수를 실행하도록 설정하는 라우트입니다. 
#이 라우트는 로그인 API 엔드포인트를 정의하며, 클라이언트가 로그인 정보를 POST 방식으로 전송할 때 이 함수가 호출되어 로그인 처리를 수행합니다.
#api 는 application programming interface의 약자로, 소프트웨어 간의 상호 작용을 가능하게 하는 인터페이스입니다. API는 특정 기능을 수행하는 함수를 제공하여 다른 소프트웨어가 해당 기능을 사용할 수 있도록 합니다. 예를 들어, 로그인 API는 사용자가 로그인할 때 필요한 기능을 제공하는 API입니다. 클라이언트는 로그인 정보를 API에 전송하고, API는 이를 처리하여 로그인 결과를 반환합니다.
# 이 코드에서 api는 




















































































    