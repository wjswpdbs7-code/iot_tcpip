# python ex11_multichat_client.py

import socket
import threading

HOST = '127.0.0.1'
PORT = 8000
#===============================================================서버로부터 메시지를 받는 함수=================================================================
def receive_messages(client, nickname): # 서버로부터 메시지를 받는 함수
    while True: # 무한 루프를 돌면서 서버로부터 메시지를 받기
        try:
            message = client.recv(1024).decode('utf-8') # 서버로부터 메시지 받기
            if message == 'NICK': # 서버가 닉네임 요청 메시지를 보냈을 때
                client.send(nickname.encode('utf-8')) # 닉네임을 서버로 전송
            else:# 서버로부터 받은 메시지가 닉네임 요청이 아닐 때
                print(message) # 서버로부터 받은 메시지 출력
        except:
            print("오류가 발생했거나, 서버와 연결이 끊어짐.") # 예외가 발생했을 때 오류 메시지 출력
            client.close() # 클라이언트 소켓 닫기
            break # 루프 탈출

#===============================================================사용자로부터 메시지를 입력받아 서버로 보내는 함수=================================================================
def write(client, nickname): # 사용자로부터 메시지를 입력받아 서버로 보내는 함수
    while True: 
        my_turn = input('me: ')# 사용자로부터 메시지 입력 받기 my_turn의 자료형은 문자열입니다 
        client.send(f"{nickname}: {my_turn}".encode('utf-8')) # 사용자로부터 메시지 입력받아 인코딩하여 서버로 전송

#===============================================================main 함수=================================================================
def main():
    nickname = input("닉네임을 입력하세요: ") # 사용자로부터 닉네임 입력 받기
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 클라이언트 소켓 생성
    client.connect((HOST, PORT)) # 서버에 연결

    receive_thread = threading.Thread(target=receive_messages, args=(client, nickname)) # 메시지 수신을 위한 스레드 생성
    receive_thread.start() # 수신 스레드 시작

    write_thread = threading.Thread(target=write, args=(client, nickname)) # 메시지 작성을 위한 스레드 생성
    write_thread.start() # 쓰기 스레드 시작

if __name__ == "__main__":
    main() 


# 인코딩 디코딩은 보낼때 인코딩, 받을때 디코딩 하는 것이 일반적입니다.
#무조건 하는가 
# 인코딩 디코딩은 문자열을 바이트로 변환하거나 바이트를 문자열로 변환하는 과정입니다. 
# 네트워크 통신에서는 데이터를 바이트 형태로 전송하기 때문에, 문자열을 보내기 전에 인코딩하여 바이트로 변환해야 합니다.
# 또한, 서버로부터 받은 메시지를 문자열로 사용하려면 디코딩하여 바이트를 문자열로 변환해야 합니다.
# 따라서, 일반적으로는 메시지를 보낼 때 인코딩하고, 메시지를 받을 때 디코딩하는 것이 일반적입니다.

#try except설명
# try except는 예외 처리를 위한 구문입니다.
# try 블록 안에는 예외가 발생할 수 있는 코드를 작성하고, except 블록 안에는 예외가 발생했을 때 실행할 코드를 작성합니다.
# 예를 들어, 클라이언트가 서버로부터 메시지를 받을 때 네트워크 오류가 발생할 수 있습니다. 이 경우, try 블록 안에서 메시지를 받는 코드를 작성하고, 