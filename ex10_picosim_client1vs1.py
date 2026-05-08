# python ex10_picosim_client1vs1.py

# 정해진 시간마다 알아서 온도를 측정해서 서버로 보내는 클라이언트 프로그램

import socket, time, random

def main():
    host = '127.0.0.1'
    port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP 소켓 생성
    try:
        client_socket.connect((host, port)) # 서버에 연결 시도
        print("Connected to server")# 연결 알림
        for _ in range(10): # 10번 반복
            current_temp = round(random.uniform(20.0, 40.0), 1) # 20.0에서 40.0 사이의 랜덤한 온도 생성, 소수점 한 자리까지 반올림 uniform 은 랜덤한 실수 생성하는 함수
            client_socket.send(str(current_temp).encode()) # 온도를 문자열로 변환해서 바이트로 인코딩한 후 서버로 전송 문자열로 변환하는 이유는 소켓 통신은 바이트 단위로 이루어지기 때문입니다. 실수로 보내는건 소켓 통신에서 지원하지 않기 때문에 문자열로 변환해서 보내는 것입니다.
            print(f"현재 온도 전송 : {current_temp}") # 전송한 온도 출력
            response = client_socket.recv(1024).decode() # 서버로부터 응답 받기, 1024는 버퍼 크기, 최대 1024바이트까지 받을 수 있음, 받은 데이터를 바이트에서 문자열로 디코딩
            if response == "MOTOR ON":# 서버로부터 받은 응답이 "MOTOR ON"이면
                print("[pico motor on]")# 모터 켜기
            elif response == "MOTOR OFF": # 서버로부터 받은 응답이 "MOTOR OFF"이면
                print("[pico motor off]")# 모터 끄기
            print("------------------------------")
            time.sleep(2) # 2초 대기

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close() # 연결이 실패하든 성공하든 소켓 닫기
        print("disconnected")
if __name__ == "__main__":
    main()

