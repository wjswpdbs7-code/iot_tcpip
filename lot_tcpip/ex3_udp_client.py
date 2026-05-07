# ex3_udp_client.py

# python ex3_udp_client.py 이번에는 코드에서 지정해서 뒤에 명령행 인자로 안받음

# UDP Datagram: 완성된 택배 박스, 비연결 지향적, 신뢰성 보장 안됨, 순서 보장 안됨

# TCP Stream: 전화 통화, 연결 지향적, 신뢰성 보장, 순서 보장

import socket, sys

def main():
    sock = socket.socket(socket.AF_INET, 
                            socket.SOCK_DGRAM) # UDP 소켓 생성
    server_addr = ("127.0.0.1", 8001) # 서버 주소 (IP, 포트) 이번에는 지정함

    sock.sendto(b"ready", server_addr) # 서버로 "ready" 메시지 전송, f가 아닌 b쓴 이유: 바이트 문자열로 보내야하기 때문
    try:
        data, addr = sock.recvfrom(1024) # 서버로부터 최대 1024바이트까지 메시지를 받는 함수, 
        print(f"Message from server : {data.decode('utf-8')}")
    except Exception as e:
        print(f"error: {e}")
    sock.close() # 소켓 닫기
if __name__ == "__main__":
    main()




        #sock.이라는것은 소켓 객체의 메서드나 속성에 접근할 때 사용하는 구문입니다. 
        #예를 들어, sock.recvfrom(1024)는 소켓 객체의 recvfrom 메서드를 호출하는 것입니다.
        # 객체선언은 언제했음? 8행에서 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)로 소켓 객체를 생성했음, 
        #객체 선언했을때 

        # 그 이후로 sock이라는 변수는 소켓 객체를 참조하게 됨, 따라서 sock.recvfrom(1024)는 그 소켓 객체의 recvfrom 메서드를 호출하는 것임