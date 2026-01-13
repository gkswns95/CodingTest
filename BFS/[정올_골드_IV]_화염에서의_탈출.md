# [정올 골드 IV] 화염에서의 탈출

> 🏷️ #너비 우선 탐색 | #그래프 이론 | #그래프 탐색 | #최단 경로 | #격자 그래프

> 🔗 https://jungol.co.kr/problem/1082?sid=8950014&cursor=OCw3LDU%3D

---

---

## 📋 문제

재우는 중간계(middle-earth)에서 유명한 용사이다.

어느날 사람들에게 부탁 받은 마물 퇴치를 신속히 해결하고 집으로 돌아가려고 하는데,

마법의 숲에서 재우를 추적하고 있던 불의 마법사 무길이와 마주치게 되었다.

무길이는 재우를 잡기 위해서 화염 마법을 시전하였고 어느덧 숲은 화염으로 가득차고 있었다.

재우는 무길이가 화염을 풀어 놓은 숲에서 신속히 용사의 집으로 귀환하고자 한다!

숲의 지도는 R행과 C열로 이루어져있다.

비어있는 칸은 '.'로 표시되고, 불은 '*'로, 바위는 'X'로 표시되어있다.

용사의 집은 'D'로 표현되고, 재우가 처음에 서있는 위치는 'S'로 표시된다.

매 분마다 재우는 인접한 4개의 칸(상, 하, 좌, 우)으로 이동할 수 있다.

불은 매 분마다 인접한 4개의 칸에 불을 옮긴다.

재우는 불과 바위를 지나지 못한다.

불은 바위와 용사의 집에 옮겨지지 않는다.

재우가 탈출을 할 수 있을 때 몇 분 만에 탈출 할 수 있는지 알아보는 프로그램을 작성하라.

---

## 📥 입력

입력의 첫번째 줄에는 50이하의 정수인 R과 C가 입력된다.

다음 줄부터 지도가 입력되며, 이는 R개의 줄로 이루어져있다.

각 R개의 줄에는 C개의 문자가 입력된다.

지도에는 정확히 하나의 용사의 집과 하나의 시작 위치가 입력된다.

---

## 📤 출력

재우가 숲에서 용사의 집으로 돌아올 수 있을 때 최단 시간(분)을 출력하고,

만약 탈출이 불가능할 경우 "impossible"을 출력한다.

---

## 💻 예제

### 예제 입력 1

```plain text
3 3
D.*
...
.S.
```

### 예제 출력 1

```plain text
3
```

---

## ✏️ 풀이

```python
# 1트 성공, 1시간
from collections import deque
import sys
input = sys.stdin.readline

r, c = map(int, input().split())

maps, player_visited, fire_visited = [], [], []
for i in range(r):
    col = []
    for j, s in enumerate(input().rstrip()):
        if s == 'S':
            sx, sy = i, j
        col.append(s)
    
    player_visited.append([False]*len(col))
    fire_visited.append([False]*len(col))
    maps.append(col)

# print(maps)
# print(visited)
# print(f'sx: {sx}, sy: {sy}')

def visualize_state(m):
    for i in range(r):
        for j in range(c):
            print(m[i][j], end=' ')
        print()
    
    print()

def bfs(x, y):
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    
    # 큐 초기화
    player_queue = deque([(x, y)])
    player_visited[x][y] = True
    
    fire_queue = deque()
    for i in range(r):
        for j in range(c):
            if maps[i][j] == '*':
                fire_queue.append((i, j))
    
    time = 0
    
    while player_queue:
        time += 1
        
        # 1. 불 먼저 확산 (현재 큐에 있는 모든 불을 한 단계 퍼뜨림)
        for _ in range(len(fire_queue)):
            fx, fy = fire_queue.popleft()
            for i in range(4):
                nx = fx + dx[i]
                ny = fy + dy[i]
                if 0 <= nx < r and 0 <= ny < c:
                    if maps[nx][ny] == '.':  # 불은 '.'으로만 퍼짐
                        maps[nx][ny] = '*'
                        fire_queue.append((nx, ny))
        
        # 2. 플레이어 이동 (현재 큐에 있는 모든 플레이어 위치를 한 단계 이동)
        for _ in range(len(player_queue)):
            cx, cy = player_queue.popleft()
            for i in range(4):
                nx = cx + dx[i]
                ny = cy + dy[i]
                
                if 0 <= nx < r and 0 <= ny < c:
                    if maps[nx][ny] == 'D':
                        return True, time
                    elif maps[nx][ny] == '.' and not player_visited[nx][ny]:
                        player_queue.append((nx, ny))
                        player_visited[nx][ny] = True
    
    return False, -1

is_arrived, cnt = bfs(sx, sy)
if is_arrived:
    print(cnt)
else:
    print('impossible')
```


