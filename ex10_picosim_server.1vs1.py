# python ex10_picosim_server.1vs1.py

# 정해진 시간마다 알아서 온도를 측정해서 서버로 보내는 클라이언트에 

# 제어 명령(온도가 30도이상이면 MOTOR ON 아니면 MOTOR OFF)을 보내는 서버 프로그램

import socket
def main():
    # 하드코딩해서 서버 IP 주소와 포트 번호를 설정
    
    host = '127.0.0.1' # 서버 IP 주소
    port = 8000 # 서버 포트 번호
    threshold = 30.0 # 모터 제어 경계 온도
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 소켓 생성
    server_socket.bind((host, port)) # 소켓에 IP 주소와 포트 번호 바인딩
    server_socket.listen(1) # 클라이언트 연결 대기, 최대 1개의 클라이언트만 허용
    print("Server started")
    conn, addr = server_socket.accept() # conn은 클라이언트와의 연결을 나타내는 새로운 소켓 객체, addr은 클라이언트의 주소 정보
    print(f"Connected by {addr}") # 클라이언트 연결 시마다 클라이언트 주소 출력
    try:
        while True:
            data = conn.recv(1024).decode() # 클라이언트로부터 데이터 받기, 1024는 버퍼 크기
            if not data:# 데이터가 없으면
                break# 루프 탈출해서 연결 종료
            temp = float(data) # 받은 데이터를 실수로 변환해서 온도로 사용
            print(f"수신 온도 : {temp}")
            if temp > threshold: # 온도가 경계 온도보다 높으면
                response = "MOTOR ON" # 모터 켜기
            else:
                response = "MOTOR OFF" # 모터 끄기
            conn.sendall(response.encode()) # 클라이언트로 응답 보내기, 바이트로 인코딩해서 전송
            print(f"제어 명령 전송 : {response}") # 제어 명령 전송 시마다 명령 출력
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close() # 클라이언트 소켓 닫기
        server_socket.close() # 서버 소켓 닫기
        print("Server end") # 서버 종료 메시지 출력

if __name__ == "__main__":
    main()

# socket.socket(socket.AF_INET, socket.SOCK_STREAM) 은 TCP 소켓을 생성하는 코드입니다.

# socket.socket() 에서 socket이라는 구조체를 이 코드 어디에서 선언한적이 없는데도 사용할 수 있는 이유는 socket 모듈을 import 했기 때문입니다.

# import함으로써 socket 모듈이 제공하는 socket 클래스와 함수들을 사용할 수 있게 됩니다.

#직역하면 socket의 객체에서 소켓 만드는 함수(구조체 이름이랑 같음(socket))를 호출하는 것인데 그 소켓의 이름을 server_socket으로 지정한 것입니다. 

#그리고 소켓에 대한 설정을 인자로 전달하는 것인데 

# socket.AF_INET는 IPv4 주소 체계를 사용하겠다는 의미입니다.

# socket.SOCK_STREAM는 TCP 소켓을 사용하겠다는 의미입니다. TCP는 연결 지향적이고 신뢰성 있는 통신을 제공합니다

# server_socket.bind((host, port))

# server_socket은 소켓 객체입니다.

#소켓 객체내에 있는 bind() 함수를 호출하고 그 함수에 (host, port) 튜플을 인자로 전달하는 것입니다.

# 현재 host는 '127.0.0.1'이고 port는 8000입니다.

# server_socket.listen(1)

# 이것은 server_socket 객체의 listen() 함수를 호출하는 코드입니다.

# 레포지토리에 현재 폴더 파일 넣는 명령어 
# 원하는 레포지토리에 현재 폴더의 파일을 넣는 명령어는 다음과 같습니다.

# https://github.com/wjswpdbs7-code/capturetans.git 여기에 현재 폴더의 파일을 넣고 싶다면
# https://github.com/wjswpdbs7-code/capturetans.git 