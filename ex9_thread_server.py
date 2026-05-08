# python ex9_thread_server.py 8000

import socket, threading, sys

def error_handling(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

def handle_client(clnt_sock, addr): #스레드가 사용할 함수, 
    print(f"Thread started for client: {addr}") # 먼저 메시지 출력 스레드가 {addr} 클라이언트를 위해 시작되었당
    try:
        while True: # 무한 루프
            data = clnt_sock.recv(1024)
            if not data: break # 메시지없으면 루프탈출
            clnt_sock.send(data) 
    except Exception as e:
        print(f"Error : {addr}, at {e}")
    finally:# 무조건 
        clnt_sock.close() # 클라이언트 소켓 닫기
        print(f"Client {addr} disconnected...") #닫은다음 {addr} 클라이언트 연결이 끊겼다고 메시지 출력

def main():
    if len(sys.argv) != 2:
        print(f"Usage : {sys.argv[0]} <port>") # 명령행 인자 개수가 2가 아니면 사용법을 출력하고 프로그램 종료
        sys.exit(1)
#=================================================step1. 소켓 생성==================================================================================================
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # TCP 소켓 생성
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 소켓 옵션 설정, SO_REUSEADDR는 소켓이 이미 사용 중인 주소에 바인딩되는 것을 허용하는 옵션
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

#================================================step4. listen====================================================================================================
    if serv_sock.listen(5) == -1: # 5는 대기 큐의 크기, 클라이언트가 동시에 여러개 접속할 수 있는데 그 중에서 몇개까지 대기할 수 있는지 설정하는 것
        error_handling("listen() error")
    print("Multi-thread server started!") # 서버 시작 메시지 출력
#================================================step5. accept====================================================================================================
    while True: 
        try:
            clnt_sock, addr = serv_sock.accept() # 클라이언트가 접속하면 accept함수가 클라이언트 소켓과 클라이언트 주소를 반환
            print(f"Connected client IP: {addr[0]}") # 클라이언트 접속 시마다 클라이언트 주소 출력 [0] 은 IP주소, [1]은 포트번호 지금은 IP주소만 출력
            t = threading.Thread(target=handle_client, args=(clnt_sock, addr)) 
            t.start() # 스레드 시작, handle_client 함수를 실행하는 새로운 스레드 생성
        except KeyboardInterrupt:
            break
    serv_sock.close() # 서버 소켓 닫기
if __name__ == "__main__":
    main()

# 1초 뒤에 KeyboardInterrupt 예외가 발생해서 서버 소켓이 닫히고 프로그램이 종료됨 컨트롤 c 안눌렀는데도 종료되는
# 이유는 serv_sock.settimeout(1.0) 때문에 1초마다 accept() 함수에서 타임아웃이 발생해서 KeyboardInterrupt 예외가 발생하기 때문입니다.
# 그렇게 하지 않게 하려면 settimeout() 함수를 제거하거나, accept() 함수에서 타임아웃이 