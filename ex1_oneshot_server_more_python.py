# ex1_onershot_server.py

# 서버 실행 : python ~server.py 8000(포트:애플리케이션 지정 숫자) 이런식으로 할거임 
# 클라 실행 : python ~client.py 127.0.0.1 (서버 IP) 8000(포트)


import socket
import sys

def main():
#=================================================step0. 명령행 인자 체크================================================================================================== 
    if len(sys.argv) != 2:
        print(f"Usage : {sys.argv[0]} <port>")
        sys.exit(1)
#=================================================step1.  주소 설정===================================================================================================
    serv_ip = '' # ''는 모든 IP주소(address enything)를 의미
    serv_port = int(sys.argv[1]) # 명령행 인자로 받은 포트 번호 ex) 8000

#=================================================step2.소켓 생성, bind, listen, accept===================================================================================================
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
    try:
        serv_sock.bind((serv_ip, serv_port))
        serv_sock.listen(5)
        print("NOW I am listening!")
        clnt_sock, clnt_addr = serv_sock.accept()
        print(f"connected from {clnt_addr}")
        message = "hello this is server speaking"
        clnt_sock.send(message.encode('utf-8'))
        clnt_sock.close() 
        
    except Exception as e:
        print(f"error: {e}")# 에러 발생했는데 내용은 e에 담겨있음, f는 %s같이 문자열 포맷팅할 때 사용하는 것, {}안에 변수 넣어서 출력할 수 있음
    finally:
        serv_sock.close()# 소켓 닫기, finally는 try-except문에서 예외가 발생하든 안하든 무조건 실행되는 블록, 여기서는 소켓을 닫는 작업을 보장하기 위해 finally 블록에 넣음



# C언어: ifndef  if__name__ == "__main__"  은 프로그램이 직접 실행될 때와 다른 모듈에서 import 될 때를 구분하기 위한 조건문입니다.
if __name__ == "__main__":

    main()

#기존 ex1_oneshot_server.py를 더 파이썬 스럽게 

# 1. 소켓 생성은 전화기를 만드는 것과 같음

# 2. 주소 설정은 전화번호를 정하는 것과 같음

# 3. bind는 전화기에 전화번호를 등록하는 것과 같음

# 4. listen은 전화기를 벨소리가 울리도록 설정하는 것과 같음

# 5. accept는 전화가 울리면 전화를 받는 것과 같음

# 6. write는 전화국 연결원이 전화로 메시지를 전달하는 것과 같음

# 다만 지금까지의 코드로는 연결원이 연결되었다고 안내하고 퇴근해버림

