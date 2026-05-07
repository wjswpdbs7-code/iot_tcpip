#ex4_echo_server.py 
#교재 112페이지에 있는 코드입니다.
#실행 python ex4_echo_server.py 

# 서버 실행 : python ~server.py 8000(포트:애플리케이션 지정 숫자) 이런식으로 할거임 
# 클라 실행 : python ~client.py 127.0.0.1 (서버 IP) 8000(포트)


import socket
import sys

def error_handling(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

def main():
#=================================================step0. 명령행 인자 체크================================================================================================== 
    if len(sys.argv) != 2:
        print(f"Usage : {sys.argv[0]} <port>")
        sys.exit(1)

#=================================================step1. 소켓 생성===================================================================================================
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
    if serv_sock.fileno() == -1:
        error_handling("socket() error")    
#=================================================step2.  주소 설정===================================================================================================
    serv_ip = '' # ''는 모든 IP주소(address enit)
    serv_port = int(sys.argv[1]) # 명령행 인자로 받은 포트 번호 ex) 8000
#==================================================step3. bind ==================================================================================================
    try:
        serv_sock.bind((serv_ip, serv_port))# ((IP주소, 포트번호)) 튜플로 묶어서 전달) 두번 묶는 이유는 bind함수의 인자가 튜플(묶음 형태)이기 때문
    except :
        error_handling("bind() error")
#================================================step4. listen, accept====================================================================================================
    if serv_sock.listen(2) == -1: # 2는 대기 큐의 크기, 책은 5인데 2로 줄임
        error_handling("listen() error")# 리신에러 났다고 알려주는 함수

    for i in range(2): # 2번 반복해서 클라이언트 접속 받음 i = 0, 1 
        try:
            clnt_sock, clnt_addr = serv_sock.accept() # 클라이언트가 접속하면 accept함수가 클라이언트 소켓과 클라이언트 주소를 반환
        except socket.error:
            error_handling("accept() error") # accept함수는 클라이언트가 접속할 때까지 블로킹(대기) 상태가 됨, 클라이언트가 접속하면 클라이언트 소켓과 주소를 반환
        print(f"Connected client {i+1}") # 클라이언트 접속 시마다 클라이언트 번호 출력, i+1로 1부터 시작하도록 함
        while True: # 클라이언트와 계속 통신하기 위해 무한 루프
            message = clnt_sock.recv(1024) # 클라이언트로부터 최대 1024바이트까지 메시지를 받는 함수, message는 받은 메시지
            if not message: # 메시지가 없으면 클라이언트가 연결을 끊은 것으로 간주하고 루프 탈출
                break
            clnt_sock.send(message) # 받은 메시지를 그대로 클라이언트에게 보내는 함수, 에코 서버이기 때문에 인코딩/디코딩 없이 그대로 보냄
        clnt_sock.close() # 클라이언트 소켓 닫기
        print(f"Client {i+1} disconnected") # 클라이언트 연결 끊김 시마다 클라이언트 번호 출력
    serv_sock.close() # 서버 소켓 닫기
#================================================step5. write() - python send()에 해당==========================================================================
    # message = "hello this is server speaking"# 클라이언트에게 보낼 메시지
    # clnt_sock.send(message.encode('utf-8'))#문자열을 바이트로 변환해서 클라이언트 소켓을 통해 메시지를 보냄, 
    # clnt_sock.close() # 클라이언트 소켓 닫기
    # serv_sock.close() # 서버 소켓 닫기

# C언어: ifndef  if__name__ == "__main__"  은 프로그램이 직접 실행될 때와 다른 모듈에서 import 될 때를 구분하기 위한 조건문입니다.
if __name__ == "__main__":
    main()


# 1. 소켓 생성은 전화기를 만드는 것과 같음

# 2. 주소 설정은 전화번호를 정하는 것과 같음

# 3. bind는 전화기에 전화번호를 등록하는 것과 같음

# 4. listen은 전화기를 벨소리가 울리도록 설정하는 것과 같음

# 5. accept는 전화가 울리면 전화를 받는 것과 같음

# 6. write는 전화국 연결원이 전화로 메시지를 전달하는 것과 같음

# 다만 지금까지의 코드로는 연결원이 연결되었다고 안내하고 퇴근해버림

#사용자 이메일 이름 구성해서 커밋하기
#git config --global user.name "홍길동"
#git config --global user.email "