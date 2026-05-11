# python ex12_flask_socket_Server.py

#web server: 고객 홈페이지같이 고객 대응 서비스를 제공하는 서버(보안, 안정성, 확장성 중요)(정적 서비스 제공)예시: 네이버, 다음, 구글, 유튜브 등
#was(web application server) : app 대응(동적 서비스 제공)예시 : 네이버 블로그, 다음 카페, 구글 드라이브, 유튜브 동영상 업로드 등

# flask : http 통신, was
# custom_thread: tcpip socket 

import socket, threading
from flask import Flask, render_template_string 
# render_template_string : 문자열로 된 HTML을 렌더링하는 함수, HTML 템플릿을 문자열로 직접 작성하여 웹 페이지를 생성할 때 사용.
# 해당 함수의 정의는 flask 라이브러리 내부에 있으며, HTML 템플릿을 문자열로 받아서 렌더링하여 최종 HTML을 반환하는 역할을 함.

app = Flask(__name__)
# 센서 데이터 저장할 전역 변수
latest_sensor_data = ""

# TCP 소켓 
def start_tcp_server(host, port):
    global latest_sensor_data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f'TCP 소켓 서버 {host}:{port}에서 대기 중')
    while True:
        client_socket, address = server_socket.accept()
        print(f'연결됨 : {address}')
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                latest_sensor_data = data.decode('utf-8')
                print(f'수신 데이터: {latest_sensor_data}')
        except Exception as e:
            print(f'Error : {e}')
        finally:
            client_socket.close()

    # flask routing 
@app.route('/')
def home():
    html = f"""
    <html> 
    <head></head>
    <h1>실시간 센서 값</h1> 
    <p>현재 값 : {latest_sensor_data}</p>
    <p> 2초마다 자동 새로 고침 중.</p>
    <script>setTimeout(function(){{location.reload();}}, 2000);</script>
    <body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    CLIENT_IP = '127.0.0.1'
    TCP_PORT = 9999
    tcp_thread = threading.Thread(target=start_tcp_server, args=(CLIENT_IP, TCP_PORT))

    tcp_thread.daemon = True # tcp_thread를 데몬 스레드(백그라운드)로 설정하여 메인 프로그램이 종료될 때 함께 종료되도록 함. 
    tcp_thread.start() # tcp_thread 시작
    app.run(host = '127.0.0.1', port = 5000) # flask 웹 서버 시작, 호스트는 로컬호스트 9999는 tcp 소켓 포트, 5000은 flask 웹 서버 포트
# http://127.0.0.1:5000

    # html = #  
    # f""" # html은 따옴표 3개로 감싸야 여러 줄 문자열이 됨.
    # <html> # html 태그는 웹 페이지의 시작과 끝을 나타냄.
    # <head></head> # head 태그는 웹 페이지의 메타데이터를 포함하는 부분으로, 예시로는 스타일 시트 링크, 스크립트 링크 등이 들어갈 수 있음. 여기서는 비어 있음. 
    # <h1>실시간 센서 값</h1> # <h1> 태그는 제목을 나타냄.
    # <p>현재 값 : {latest_sensor_data}</p> # <p> 태그는 단락을 나타냄. 
    # <p> 2초마다 자동 새로 고침 중.</p>
    # <script>setTimeout(function{{location.reload();}}, 2000);</script> <script> 태그는 자바스크립트 코드를 포함하는 부분. setTimeout 함수는 일정 시간 후에 페이지를 새로 고침하도록 설정.
    # <body>
    # </html>
    # """

