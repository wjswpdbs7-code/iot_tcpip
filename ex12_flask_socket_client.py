# python ex12_flask_socket_client.py

import socket, time, random

def main():
    SERVER_IP = '127.0.0.1' 
    SERVER_PORT = 9999

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client_socket.connect((SERVER_IP, SERVER_PORT)) 
        print(f'서버 {SERVER_IP}:{SERVER_PORT}에 연결 됨.')
        while True:
            temp = random.uniform(20.0, 30.0)
            message = f'온도 : {temp:.2f}°C'
            client_socket.sendall(message.encode('utf-8'))
            print(f'보낸 데이터: {message}')
            time.sleep(3) 
            
    except Exception as e:
        print('Error:', e)

    finally:
        client_socket.close()

if __name__ == '__main__':
    main()


# mcu로 가정하여 스레드는 여기에는 필요없음.