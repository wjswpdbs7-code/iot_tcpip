# ex3_udp_client.py

# python ex3_udp_client.py 이번에는 코드에서 지정해서 뒤에 명령행 인자로 안받음

# UDP Datagram: 완성된 택배 박스, 비연결 지향적, 신뢰성 보장 안됨, 순서 보장 안됨

# TCP Stream: 전화 통화, 연결 지향적, 신뢰성 보장, 순서 보장

import socket, sys

def main():
    sock = socket.socket(socket.AF_INET, 
                            socket.SOCK_DGRAM) # UDP 소켓 생성
    # server_addr = ("127.0.0.1", 8001) # 서버 주소 (IP, 포트) 이번에는 지정함 127.0.0.1은 자기자신의 IP주소
    server_addr = ("163.152.213.105", 8001) # 옆자리에 있는 컴퓨터의 IP주소로 변경  

    sock.sendto(b"ready", server_addr) # 서버로 "ready" 메시지 전송, f가 아닌 b쓴 이유: 바이트 문자열로 보내야하기 때문
    try:
        data, addr = sock.recvfrom(1024) # 서버로부터 최대 1024바이트까지 메시지를 받는 함수, 
        print(f"Message from server : {data.decode('utf-8')}")
    except Exception as e:
        print(f"error: {e}")
    sock.close() # 소켓 닫기
if __name__ == "__main__":
    main()



# 현재 코드의 진행 흐름

#1. 소켓 객체 생성: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# UDP 소켓을 생성하고, sock이라는 변수에 할당
# 2. 서버 주소 설정: server_addr = ("163.152.213.105", 8001)
# 서버의 IP 주소와 포트 번호를 튜플 형태로 저장(튜플: 여러 개의 값을 하나로 묶어서 저장하는 자료형, 소괄호로 감싸서 표현) 

        #sock.이라는것은 소켓 객체의 메서드나 속성에 접근할 때 사용하는 구문입니다. 
        #예를 들어, sock.recvfrom(1024)는 소켓 객체의 recvfrom 메서드를 호출하는 것입니다.
        # 객체선언은 언제했음? 8행에서 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)로 소켓 객체를 생성했음, 
        #객체 선언했을때 

        # 그 이후로 sock이라는 변수는 소켓 객체를 참조하게 됨, 따라서 sock.recvfrom(1024)는 그 소켓 객체의 recvfrom 메서드를 호출하는 것임

        # server_addr = ("163.152.213.105", 8001) 이거 변수 배열로 한거 아니고 하나는 문자열 하나는 숫자인데 
        #어케 저장한거임 : 