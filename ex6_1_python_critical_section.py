#python ex6_1_python_critical_section.py 

# 임계영역 = 공유 자원에 접근하는 코드 영역
# 공유자원을 은행 잔고로 비유해서 이해해보자

import threading

total_balance = 0 # 은행 잔고를 나타내는 변수, 여러 스레드가 공유하는 자원

def deposit(amount):# 입금하는 함수, amount는 입금할 금액
    global total_balance # total_balance 변수를 전역 변수로 사용하겠다는 선언
    for i in range(amount): # amount 만큼 반복해서 입금하는 시뮬레이션
        total_balance += 1 # total_balance에 1씩 더하는 작업,

if __name__ == "__main__":
    t1 = threading.Thread(target=deposit, args=(1000000,)) # deposit 함수를 실행하는 스레드 t1 생성, 1000000을 입금할 금액으로 전달
    t2 = threading.Thread(target=deposit, args=(1000000,)) # deposit 함수를 실행하는 스레드 t2 생성, 1000000을 입금할 금액으로 전달

    t1.start() # 스레드 t1 시작
    t2.start() # 스레드 t2 시작
    t1.join() # t1 스레드가 종료될 때까지 대기
    t2.join() # t2 스레드가 종료될 때까지 대기
    print(f"최종 잔액: {total_balance}원") # 최종 잔액 출력
    print("예상 잔액: 2000000원") # 예상 잔액 출력


