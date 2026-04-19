# [프로그래머스 LV. 3] N으로 표현

---

# 문제 설명

### **문제 설명**

아래와 같이 5와 사칙연산만으로 12를 표현할 수 있습니다.

12 = 5 + 5 + (5 / 5) + (5 / 5)

12 = 55 / 5 + 5 / 5

12 = (55 + 5) / 5

5를 사용한 횟수는 각각 6,5,4 입니다. 그리고 이중 가장 작은 경우는 4입니다.

이처럼 숫자 N과 number가 주어질 때, N과 사칙연산만 사용해서 표현 할 수 있는 방법 중 N 사용횟수의 최솟값을 return 하도록 solution 함수를 작성하세요.

### 제한사항

- N은 1 이상 9 이하입니다.
- number는 1 이상 32,000 이하입니다.
- 수식에는 괄호와 사칙연산만 가능하며 나누기 연산에서 나머지는 무시합니다.
- 최솟값이 8보다 크면 -1을 return 합니다.
### 입출력 예

### 입출력 예 설명

예제 #1

문제에 나온 예와 같습니다.

예제 #2

`11 = 22 / 2`와 같이 2를 3번만 사용하여 표현할 수 있습니다.

---

# 풀이 (1시간 30분 소요)

> 문제를 읽고 약 30분 정도 고민을 해보았지만 문제 풀이의 방향성이 전혀 잡히지 않았다. 결국 페이지 상단에 있는 유튜브 강의를 보고 해결했다. 동적 프로그래밍 문제의 핵심은 결국 문제를 어떻게 풀어야 할 지를 잘 설계해야 하는 것을 느꼈다. 실전에서 써먹으려면 앞으로 더 많은 유형의 문제를 풀어보면서 생각의 폭을 더 넓혀야 할 것 같다.

```python
# 핵심 아이디어: N이 쓰이는 개수 n_N (1~8)에 따른 경우의 수를 차례로 구하면서 해답 찾기
# 예시: 
# N=5, n_N = 1일 때: Set1 = {5}
# N=5, n_N = 2일 때: Set2 = {55, 5+5, 5-5, 5*5, 5//5}
# => A [+, -, *, //] B 구조에서 A, B가 각각 Set1, Set1이 된 것
# N=5, n_N = 3일 때: {555, 5+55, 5-55, 5*55, 5//55, 5+(5+5), ...}
# => A [+, -, *, //] B 구조에서 (A,B) = [(Set1, Set2), (Set2, Set1)]
# 종료 조건: 각 n_N의 경우의 수 찾기가 끝났을 때, "number"가 계산되었는지 체크

def solution(N, number):
    if N == number:
        return 1
    else:
        answer = -1
        
    # 1. Init: N을 한번 쓰는 경우(Set1), ..., 여덟 번 쓰는 경우(Set8)
    set_list = []
    for i in range(8):
        set_list.append(set())
    for i in range(8):
        set_list[i].add(int(str(N) * (i+1)))
    
    # print(f"set_list: {set_list}")
    
    # 2. Main loop
    for i in range(1, len(set_list)):
        for j in range(i):
            for A in set_list[j]:
                for B in set_list[i-j-1]:
                    set_list[i].add(A + B)
                    set_list[i].add(A - B)
                    set_list[i].add(A * B)
                    if B != 0:
                        set_list[i].add(A // B)
        
        if number in set_list[i]:
            answer = i + 1
            break
    
    return answer
```


