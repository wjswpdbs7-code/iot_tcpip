# python ex7_python_asyncio.py

import asyncio# 비동기 I/O를 지원하는 라이브러리, 비동기 프로그래밍을 할 때 사용
import time # 시간 관련 함수 라이브러리

async def brew_coffee(name, duration):# 어떤 커피를 어느 시간만큼 만들거임 
    print(f"{name} 커피 주문 접수, {duration}초 걸려용")
    await asyncio.sleep(duration) # await는 비동기 함수에서 다른 작업이 실행될 수 있도록 하는 키워드, asyncio.sleep(duration)은 duration 초 동안 대기하는 비동기 함수, 이 동안 다른 작업이 실행될 수 있음
    print(f"{name} 커피 완성!")
    return f"{name} 커피"

async def main():
    print("-- 카페 오픈 --")
    start_time = time.time() # 시작 시간 기록

    task1 =  brew_coffee("아이수 아메리카노", 3)
    task2 =  brew_coffee("라떼", 2)
    task3 =  brew_coffee("스무디", 1)

    results = await asyncio.gather(task1, task2, task3) 

    #results에 asyncio(비동기: 한`번에)모률을 쓰는데 gather는 여러 개의 비동기 함수를 동시에 실행-> 끝날 때까지 대기 (이 역할을 하는 것은 await)-> 결과를 리스트로 반환

    end_time = time.time() # 종료 시간 기록
    print(f"총 소요 시간: {end_time - start_time}초") # 총 소요 시간 출력, 소수점 둘째 자리까지 표시
    print(f"받은 음료: {results}") # 받은 음료 출력

if __name__ == "__main__":
    asyncio.run(main()) # asyncio.run()은 비동기 함수를 실행하는 함수, main() 함수를 실행하여 비동기 작업을 시작


    
#if __name__ == "__main__"
# C언어: ifndef  if__name__ == "__main__"  은 프로그램이 직접 실행될 때와 다른 모듈에서 import 될 때를 구분하기 위한 조건문입니다.
# 쉽게 말하면 if __name__ == "__main__"은 이 파일이 직접 실행될 때만 main() 함수를 실행하라는 의미입니다.
# 이 구문 이 없으면 이 파일이 다른 파일에서 import 될 때도 main() 함수가 실행될 수 있습니다.
# 단독으로 쓸꺼면 없어도 실행 가능


# def main():과 if __name__ == "__main__": main()의 차이점

# def main():은 main이라는 함수를 정의하는 것입니다. 이 함수는 프로그램의 주요 로직을 담고 있습니다. 
# if __name__ == "__main__": main()은 이 파일이 직접 실행될 때 main() 함수를 호출하는 것입니다.
# 이렇게 하면 이 파일이 다른 파일에서 import 될 때 main() 함수가 자동으로 실행되는 것을 방지할 수 있습니다.
# if __name__ == "__main__": main()을 직역하면 "이름이 __main__인 경우 main() 함수를 실행하라"