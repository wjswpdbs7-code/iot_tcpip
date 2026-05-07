# ex2_oneshot_client_every1byte.py

# 서버 실행 : python ~server.py 8000(포트:애플리케이션 지정 숫자) 이런식으로 할거임 
# 클라 실행 : python ~client.py 127.0.0.1 (서버 IP) 8000(포트)


import socket, sys

def error_handling(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

def main():
#=================================================step0. 명령행 인자 체크==================================================================================================

    if len(sys.argv) != 3: # 3인 이유는 프로그램 이름, 서버 IP, 포트 번호 총 3개이기 때문 (4행 참고)
        print(f"Usage : {sys.argv[0]} <IP> <port>")
        sys.exit(1)
#=================================================step1. 소켓 생성===================================================================================================

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         0)
    if sock.fileno() == -1:
        error_handling("socket() error")# 소켓 생성 실패 시 소켓 생성에서 에러가 발생했다고 알려주는 함수
#=================================================step2. 서버 주소 설정===================================================================================================

    serv_ip = sys.argv[1] # 명령행 인자로 받은 서버 IP 주소 ex) 127.0.0.1
    serv_port = int(sys.argv[2]) # 명령행 인자로 받은 포트 번호 ex) 8000
#==================================================step3. connect==================================================================================================

    try:
        sock.connect((serv_ip, serv_port)) # 서버 IP와 포트 번호를 튜플로 묶어서 connect 함수에 전달, 서버에 연결 시도
    except :
        error_handling("socket connect() error") # 연결 실패 시 소켓 연결에서 에러가 발생했다고 알려주는 함수
#===================================================step4. read()  =================================================================================================

    # try:
    #     message_from_server = sock.recv(30) # 서버로부터 메시지를 받는 함수, 30은 버퍼 크기, 최대 30바이트까지 받을 수 있음
    #     if not message_from_server: # 메시지를 받지 못했을 때 (빈 문자열이 반환될 때)
    #         error_handling("no contents error") # 서버로부터 메시지를 받지 못했다고 알려주는 함수
    #     print(f"Message from server : { \
    #         message_from_server.decode('utf-8') \
    #     }") # 서버로부터 받은 메시지를 바이트에서 문자열로 디코딩해서 출력
    # except socket .error:
    #     error_handling("read() error") # 메시지를 받는 과정에서 에러가 발생했다고 알려주는 함수

#===================================================step4. read() 이번엔 1바이트씩 읽는걸로 바꿔보자 =================================================================================================

    message_buffer = bytearray(30) # 최대 30바이트까지 받을 수 있는 버퍼 배열 생성
    str_len = 0 # 받은 메시지의 길이를 저장할 변수 초기화
    idx = 0 # 버퍼에 메시지를 저장할 때 사용할 인덱스 초기화

    while True:
        read_byte = sock.recv(1) # 1바이트씩 메세지 읽기
        if not read_byte: # 메시지를 받지 못했을 때 (빈 문자열이 반환될 때)
            break # 탈출
        message_buffer[idx] = read_byte[0] # 버퍼에 읽은 바이트 저장, read_byte는 bytes 객체이므로 인덱싱해서 첫 번째 바이트를 가져와서 저장
        idx += 1 # 인덱스 증가 
        str_len += 1 # 받은 메시지의 길이 증가 파이썬에는 ++이 읎어서 idx += 1로 표현해야함;;
    received_message = message_buffer[:idx].decode('utf-8')# 받은 메세지 버퍼에서 실제로 받은 메시지 부분만 슬라이싱해서 문자열로 디코딩
    print(f"Message from server : {received_message}") # 서버로부터 받은 메시지 출력
    print(f"Function read call count : {str_len}") # 받은 메시지의 길이 출력, 실제로 받은 메시지의 길이와 같음

    sock.close() # 소켓 닫기 

if __name__ == "__main__":
    main()



# 파이썬 용어

# print(f"문자열 {변수} 문자열") : f-string, 문자열 안에 {}로 변수 값을 삽입할 수 있는 기능 %d %s대신 f만 해도 다른 타입의 변수도 가능