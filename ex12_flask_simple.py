# python ex12_flask_simple.py

#pip install flask

from flask import Flask, request # flask 모듈에서 Flask 클래스와 request 객체를 가져옵니다.

app = Flask(__name__) # Flask 애플리케이션 객체를 생성합니다. __name__은 현재 모듈의 이름 즉 현재 파일의 이름을 나타냅니다.

@app.route('/') # '/' 경로에 대한 라우트를 정의합니다. 이 경로는 웹사이트의 루트 URL을 나타냅니다. 
def home(): # home 함수는 '/' 경로에 대한 요청이 들어왔을 때 실행됩니다.
    return "Wow!" # home 함수는 "Wow!"라는 문자열을 반환합니다. 따라서 사용자가 웹사이트의 루트 URL에 접속하면 "Wow!"라는 메시지를 볼 수 있습니다.

if __name__ == '__main__': # 이 조건문은 현재 모듈이 직접 실행될 때만 아래의 코드를 실행하도록 합니다. 
    app.run(host='127.0.0.1', port=5000) 
    #http
    # Flask 애플리케이션을 실행합니다. host는 서버가 바인딩할 IP 주소를 지정하고, port는 서버가 수신할 포트 번호를 지정합니다. 
    # 5000 = 기본적으로 Flask가 사용하는 포트입니다.



# 라우트란 웹 애플리케이션에서 URL과 해당 URL에 대한 처리를 연결하는 것을 말합니다.
#형식
# @app.route('/경로')
# def 함수명():

# @app.route('/') : 루트 경로에 대한 라우트를 정의합니다. 즉, 웹사이트의 기본 URL에 대한 요청이 들어왔을 때 home 함수가 실행됩니다.
#('/') : 
# def home(): : home 함수는 '/' 경로에 대한 요청이 들어왔을 때 실행됩니다. 이 함수는 "Wow!"라는 문자열을 반환합니다. 
# 따라서 사용자가 웹사이트의 루트 URL에 접속하면 "Wow!"라는 메시지를 볼 수 있습니다.

# 파이썬 for 문 
# for i in range(5):
#     print(i)

