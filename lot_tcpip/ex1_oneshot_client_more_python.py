# ex1_oneshot_client.py

# 서버 실행 : python ~server.py 8000(포트:애플리케이션 지정 숫자) 이런식으로 할거임 
# 클라 실행 : python ~client.py 127.0.0.1 (서버 IP) 8000(포트)


import socket, sys

def main():
#=================================================step0. 명령행 인자 체크==================================================================================================

    if len(sys.argv) != 3: # 3인 이유는 프로그램 이름, 서버 IP, 포트 번호 총 3개이기 때문 (4행 참고)
        print(f"Usage : {sys.argv[0]} <IP> <port>")
        sys.exit(1)
#=================================================step1. 주소 설정===================================================================================================
    serv_ip = sys.argv[1] # 명령행 인자로 받은 서버 IP 주소 ex) 127.0.0.1 sys.argv
    serv_port = int(sys.argv[2]) # 명령행 인자로 받은 포트 번호 ex) 8000
#=================================================step2. 소켓 생성===================================================================================================

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         0)
    try:
        sock.connect((serv_ip, serv_port))
        message_from_server = sock.recv(1024) # 서버로부터 최대 1024바이트까지 메시지를 받음,인터넷 표준 버퍼 크기
        if not message_from_server: # 메시지를 받지 못했을 때 (빈 문자열이 반환될 때) if not 은 c언어에서의 if(message_from_server == "")와 같은 의미 
            print("no contents error") # 서버로부터 메시지를 받지 못했다고 알려주는 함수
        print(f"Message from server : { \
            message_from_server.decode('utf-8') \
        }")
    except Exception as e:
        print(f"error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()



# 1. 소켓 생성은 전화기를 만드는 것과 같음

# 2. 주소 설정은 전화번호를 정하는 것과 같음

# 3. connect는 전화로 상대방에게 전화를 거는 것과 같음

# 4. read는 전화를 통해 상대방이 말하는 메시지를 듣는 것과 같음

# 지금까지의 코드는 전화기로 전화국 연결원에게 전화를 걸어서 연결이 되었다고 안내받는 과정까지입니다
# (실제로는 연결은 아직 안된 상태입니다, 연결이 되었다고 메세지만 안내받은 상태입니다)

# ex1_oneshot_server_more_python.py에서는 연결이 되었다고 안내받은 후에 연결원이 전화로 메시지를 전달하는 과정까지 구현

#ex1_oneshot_client_more_python.py에서는 연결원이 전화로 메시지를 전달하는 과정까지 구현한 서버에 클라이언트가 접속해서 메시지를 받는 과정까지 구현 


# 주소와 포트 번호에 대하여

# IP 주소는 네트워크 상에서 컴퓨터를 식별하는 고유한 번호입니다. 예를 들어, 192.168.0.1

