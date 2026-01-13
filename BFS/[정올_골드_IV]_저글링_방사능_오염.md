# [정올 골드 IV] 저글링 방사능 오염

> 🏷️ #너비 우선 탐색 | #그래프 이론 | #그래프 탐색 | #최단 경로 | #격자 그래프

> 🔗 https://jungol.co.kr/problem/1078?cursor=OCw3LDE%3D

---

---

## 📋 문제

승훈이는 심심한 시간에 스타크래프트(Starcraft) 게임을 하며 놀고 있었다.

스타크래프트 유닛중 하나인 저글링을 한 곳에 몰아세운 뒤, 방사능 오염 공격으로 없애보려고 했다.

그런데 좀 더 재미있게 게임을 하기 위해서 게임을 개조하여 방사능 오염 공격을 가하면 방사능은 1초마다 이웃한 저글링에 오염된다.

그리고 방사능에 오염된 저글링은 3초 후에 죽게 된다.

예를 들어 아래 왼쪽그림과 같이 모여 있는 저글링 중에 빨간 동그라미 표시를 한 저글링에게 방사능 오염공격을 가하면,

총 9초 후에 모든 저글링들이 죽게 된다. 아래 오른쪽에 있는 그림의 숫자들은 각 저글링들이 죽는 시간이다.

저글링을 모아놓은 지도의 크기와 지도상에 저글링들이 놓여 있는 격자 위치가 주어질 때,

총 몇 초 만에 저글링들을 모두 없앨 수 있는지 알아보는 프로그램을 작성하시오.

---

## 📥 입력

첫째 줄은 지도의 열의 크기와 행의 크기가 주어진다. 지도는 격자 구조로 이루어져 있으며 크기는 100×100칸을 넘지 않는다.

둘째 줄부터는 지도상에 저글링들이 놓여있는 상황이 주어진다. 1은 저글링이 있는 곳의 표시이고 0은 없는 곳이다.

마지막 줄에는 방사능오염을 가하는 위치가 열 번호 행 번호 순으로 주어지며 **x, y 좌표의 시작은 1이다**.

---

## 📤 출력

죽을 수 있는 저글링들이 모두 죽을 때까지 몇 초가 걸리는지 첫 번째 줄에 출력하고 둘째 줄에는 죽지 않고 남아 있게 되는 저글링의 수를 출력하

---

## 💻 예제

### 예제 입력 1

```plain text
7 8 
0010000 
0011000 
0001100 
1011111 
1111010 
0011110 
0011100 
0001000 
3 5
```

### 예제 출력 1

```plain text

9 
0
```

---

## ✏️ 풀이

```python
# 1트 성공, 40분
from collections import deque

import sys
input = sys.stdin.readline

m, n = map(int, input().split())

graph, visited = [], []
for i in range(n):
    col = [int(c) for c in input().rstrip()]
    graph.append(col)
    visited.append([False] * len(col))

# print(graph)
# print(visited)

sy, sx = map(int, input().split())

# print(sx, sy)

def bfs(x, y):
    queue = deque([(x, y, 1)])
    visited[x][y] = True
    graph[x][y] = 0

    while queue:
        cur_x, cur_y, cur_group = queue.popleft()

        # print(f'cur_group: {cur_group}')

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]

            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and graph[nx][ny] == 1:
                    queue.append((nx, ny, cur_group+1))
                    visited[nx][ny] = True
                    graph[nx][ny] = 0
    
    return cur_group

last_group = bfs(sx-1, sy-1)
print(last_group + 2)
print(sum(sum(v) for v in graph))
```


