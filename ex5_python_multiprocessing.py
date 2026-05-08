#python ex5_python_multiprocessing.py

import multiprocessing, time

# 병렬적으로 실행할 무거운 작업
def heavy_work(n):
    time.sleep(1)  # 1초 대기 (무거운 작업 수행한다고 가정하는 시뮬레이션)
    result = n * n  # 제곱 계산
    print(f"숫자 {n} 계산 완료: {result}")
    return result
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8] # 계산할 숫자 리스트
    print("--멀티 프로세싱 시작--")
    start_time = time.time() # 시작 시간 기록
    with multiprocessing.Pool(processes=4) as pool: # 뜻: multiprocessing 모듈의 Pool 클래스를 사용하여 프로세스 풀을 생성, with 구문을 사용하여 자동으로 자원 관리
        results = pool.map(heavy_work, numbers) # heavy_work 함수를 numbers 리스트의 각 요소에 병렬적으로 적용
    end_time = time.time() # 종료 시간 기록
    print(f"최종 결과: {results}") # 계산 결과 출력
    print(f"총 소요 시간: {end_time - start_time:.2f}초") # 총 소요 시간 출력, 소수점 둘째 자리까지 표시 