#python ex6_python_threading.py

import threading, time

def download_data(site_name, delay):
    print(f"{site_name} 다운로드 시작...")
    time.sleep(delay) # delay 초 동안 대기, 다운로드 시뮬레이션
    print(f"{site_name} 다운로드 완료!: {delay}초 소요")

if __name__ == "__main__":
    sites = [("Google", 2), ("Naver", 3), ("Github", 1), ("Youtube", 2)]# 다운로드할 사이트,시간(초)을 튜플로 묶어서 리스트로 저장    
    threads = [] # 스레드를 저장할 리스트
    print("--멀티 스레딩 시작--")
    start_time = time.time() # 지금 시간을 start_time에 저장

    for site_name, delay in sites: # sites 리스트에서 사이트 이름과 지연 시간을 하나씩 꺼내서 반복 4번 반복
        thread = threading.Thread(target=download_data, args=(site_name, delay)) # download_data 함수를 실행하는 스레드 생성, args로 사이트 이름과 지연 시간을 전달
        threads.append(thread)# 생성된 스레드를 threads 리스트에 추가
        thread.start()

    for thread in threads: # 생성된 모든 스레드가 작업을 완료할 때까지 종료 대기
        thread.join()

    end_time = time.time() # 지금 시간을 end_time에 저장
    print(f"총 소요 시간: {end_time - start_time}초") # 총 소요 시간 출력, 소수점 둘째 자리까지 표시 
    
# 동기 비동기 방식 설명
# 동기 방식은 작업이 순차적으로 실행되는 방식입니다. 예시: A 작업이 끝나야 B 작업이 시작되는 방식입니다.
# 비동기 방식은 작업이 동시에 실행되는 방식입니다. 예시: A 작업과 B 작업이 동시에 실행되는 방식입니다.