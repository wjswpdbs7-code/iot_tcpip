# python ex9_thread_client.py 127.0.0.1 8000

import socket, threading, sys

def send_msg(sock):
    while True:
        message = input("your message : (q to end) ") # 사용자로부터 메시지 입력 받음
        if message.lower() == 'q': # 메시지가 'q'나 'Q'이면 루프 탈출
            sock.close() # 소켓 닫기
            break
        sock.send(message.encode('utf-8')) # 메시지를 바이트로 인코딩해서 소켓을 통해 서버로 보냄

def recv_msg(sock):
    while True:
        try:
            data = sock.recv(1024) # 서버로부터 메시지를 받는 함수, 1024는 버퍼 크기, 최대 1024바이트까지 받을 수 있음
            if not data: # 메시지를 받지 못했을 때 (빈 문자열이 반환될 때)
                break 
            print(f"Received : {data.decode('utf-8')}") # 서버로부터 받은 메시지를 바이트에서 문자열로 디코딩해서 출력
        except socket.error:
            break

def main():
#=================================================step0. 명령행 인자 체크==================================================================================================

    if len(sys.argv) != 3: # 3인 이유는 프로그램 이름, 서버 IP, 포트 번호 총 3개이기 때문 
        print(f"Usage : {sys.argv[0]} <IP> <port>")
        sys.exit(1)
#=================================================step1. 소켓 생성===================================================================================================

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         0)
#=================================================step2. 서버 주소 설정===================================================================================================

    serv_ip = sys.argv[1] # 명령행 인자로 받은 서버 IP 주소 ex) 127.0.0.1
    serv_port = int(sys.argv[2]) # 명령행 인자로 받은 포트 번호 ex) 8000
#==================================================step3. connect==================================================================================================

    try:
        sock.connect((serv_ip, serv_port)) # 서버 IP와 포트 번호를 튜플로 묶어서 connect 함수에 전달, 서버에 연결 시도
    except :
        print("connect() error") 
        return
#===================================================step4. read() =================================================================================================
    snd = threading.Thread(target=send_msg, args=(sock,)) # send_msg 함수를 실행하는 스레드 생성, sock을 인자로 전달
    rcv = threading.Thread(target=recv_msg, args=(sock,)) # recv_msg 함수를 실행하는 스레드 생성, sock을 인자로 전달
    snd.start() # send_msg 스레드 시작
    rcv.start() # recv_msg 스레드 시작
    snd.join() # send_msg 스레드가 종료될 때까지 대기
    print("Client terminated...") # send_msg 스레드가 종료된 후 클라이언트 종료 메시지 출력
    
if __name__ == "__main__":
    main()




    # snd = threading.Thread(target=send_msg, args=(sock,)) 이 구조는 send_msg 함수를 실행하는 스레드를 생성하는 코드입니다.