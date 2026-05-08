# python ex8_multiproc_server.py 8000
# python ex4_echo_client.py 127.0.0.1 8000

import socket, multiprocessing, os, sys

def error_handling(message):# 에러 메시지를 표준 에러로 출력하고 프로그램을 종료하는 함수
    sys.stderr.write(message + '\n')
    sys.exit(1)

def handle_client(clnt_sock, addr):# 클라이언트 소켓을 인자로 받아서 클라이언트와 통신하는 함수
    print(f"child process handling client: {addr}") # 클라이언트 주소 출력 자식 프로

    try:
        while True: # 클라이언트와 계속 통신하기 위해 무한 루프
            data = clnt_sock.recv(1024) # 클라이언트로부터 최대 1024바이트까지 메시지를 받는 함수, data는 받은 메시지
            if not data: # 메시지가 없으면 클라이언트가 연결을 끊은 것으로 간주하고 루프 탈출
                break
            clnt_sock.send(data) # 받은 메시지를 그대로 클라이언트에게 보내는 함수, 에코 서버이기 때문에 인코딩/디코딩 없이 그대로 보냄
    
    finally:
        clnt_sock.close() # 클라이언트 소켓 닫기
        print(f"child{addr} disconnected...") # 클라이언트 연결 끊김 시마다 클라이언트 주소 출력

def main():
#=================================================step0. 명령행 인자 체크==================================================================================================
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
    serv_sock.settimeout(1.0) # 소켓에 타임아웃 설정 1초마다 빠져나와 신호 확인
#================================================step4. listen====================================================================================================
    serv_sock.listen(2) # 2는 대기 큐의 크기, 클라이언트가 동시에 여러개 접속할 수 있는데 그 중에서 몇개까지 대기할 수 있는지 설정하는 것
    print("Multi-process server started!") # 서버 시작 메시지 출력
#================================================step5. accept====================================================================================================
    while True: # 클라이언트 접속을 계속 받기 위해 무한 루프 
        try:
            try: 
                clnt_sock, clnt_addr = serv_sock.accept() # 클라이언트가 접속하면 accept함수가 클라이언트 소켓과 클라이언트 주소를 반환 
                print(f"new client connected") # 클라이언트 접속 시마다 메시지 출력
            except socket.timeout:
                continue # accept 함수가 타임아웃되면 계속해서 다음 클라이언트 접속을 기다림
        except KeyboardInterrupt:
            break # 키보드 인터럽트(예: Ctrl+C)가 발생하면 루프 탈출 근데 안되는 
        except Exception:
            continue # 다른 예외가 발생하면 계속해서 다음 클라이언트 접속을 기다림

        #fork() 함수를 사용하여 새로운 프로세스를 생성, 자식 프로세스에서는 클라이언트와 통신하는 handle_client 함수를 실행
        p = multiprocessing.Process(target=handle_client, args=(clnt_sock, clnt_addr)) 
        # handle_client 함수를 실행하는 새로운 프로세스 생성, args로 클라이언트 소켓과 주소 전달(target = 실행할 함수, args = (함수에 전달할 인자1, 인자 2))
        
        p.start() # 생성된 프로세스 시작
        clnt_sock.close() # 부모 프로세스에서는 클라이언트 소켓을 닫음, 자식 프로세스에서 클라이언트와 통신하기 때문에 부모 프로세스에서는 소켓을 닫아야 함
    serv_sock.close() # 서버 소켓 닫기

if __name__ == "__main__":
    main()

#이 코드는 멀티프로세싱을 사용하여 여러 클라이언트를 동시에 처리하는 TCP 서버입니다.

# timeout과 KeyboardInterrupt 예외 처리 설명

# timeout 예외는 accept 함수가 설정된 시간(1초) 동안 클라이언트 접속을 기다리다가

# 클라이언트가 접속하지 않으면 발생하는 예외입니다. 이 예외가 발생하면 continue 문을 실행하여 다음 클라이언트 접속을 계속 기다립니다.

# KeyboardInterrupt 예외는 사용자가 키보드 인터럽트(예: Ctrl+C)를 발생시켰을 때 발생하는 예외입니다. 

# 이 예외가 발생하면 break 문을 실행하여 루프를 탈출하고 서버를 종료합니다.

# timeout없이 keyboardinterrupt 예외 처리만 하면 ctrl+c로 서버를 종료할 때

# accept 함수가 클라이언트 접속을 기다리면서 블로킹 상태가 되기 때문에 키보드 인터럽트가 발생해도 서버가 즉시 종료되지 않고 

# accept 함수가 클라이언트 접속을 기다리는 동안 블로킹 상태가 되어서 키보드 인터럽트가 발생해도 서버가 즉시 종료되지 않는 문제가 발생할 수 있습니다.
