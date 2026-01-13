# [정올 골드 IV] 토마토(초)

> 🏷️ #너비 우선 탐색 | #그래프 이론 | #그래프 탐색 | #최단 경로 | #격자 그래프

> 🔗 https://jungol.co.kr/problem/2606?cursor=MTAsNSww

---

---

## 📋 문제

철수의 토마토 농장에서는 토마토를 보관하는 큰 창고를 가지고 있다.

토마토는 아래의 그림과 같이 격자모양 상자의 칸에 하나씩 넣은 다음,

상자들을 수직으로 쌓아 올려서 창고에 보관한다.

창고에 보관되는 토마토들 중에는 잘 익은 것도 있지만, 아직 익지 않은 토마토들도 있을 수 있다.

보관 후 하루가 지나면, 익은 토마토들의 인접한 곳에 있는 익지 않은 토마토들은 익은 토마토의 영향을 받아 익게 된다.

하나의 토마토에 인접한 곳은 위, 아래, 왼쪽, 오른쪽, 앞, 뒤 여섯 방향에 있는 토마토를 의미한다.

대각선 방향에 있는 토마토들에게는 영향을 주지 못하며, 토마토가 혼자 저절로 익는 경우는 없다고 가정한다.

철수는 창고에 보관된 토마토들이 며칠이 지나면 다 익게 되는지 그 최소 일수를 알고 싶어 한다.

토마토를 창고에 보관하는 격자모양의 상자들의 크기와 익은 토마토들과 익지 않은 토마토들의 정보가 주어졌을 때,

며칠이 지나면 토마토들이 모두 익는지, 그 최소 일수를 구하는 프로그램을 작성하라.

단, 상자의 일부 칸에는 토마토가 들어있지 않을 수도 있다.

---

## 📥 입력

입력파일의 첫 줄에는 상자의 크기를 나타내는 두 정수 M, N과 쌓아올려지는 상자의 수를 나타내는 H가 주어진다.

M은 상자의 가로 칸의 수, N은 상자의 세로 칸의 수를 나타낸다. 단, 2≤M≤100, 2≤N≤100, 1≤H≤100이다.

둘째 줄부터는 가장 밑의 상자부터 가장 위의 상자까지에 저장된 토마토들의 정보가 주어진다.

즉, 둘째 줄부터 N개의 줄에는 하나의 상자에 담긴 토마토의 정보가 주어진다.

각 줄에는 상자 가로줄에 들어있는 토마토들의 상태가 M개의 정수로 주어진다.

정수 1은 익은 토마토, 정수 0은 익지 않은 토마토, 정수 -1은 토마토가 들어있지 않은 칸을 나타낸다.

이러한 N개의 줄이 H번 반복하여 주어진다.

---

## 📤 출력

여러분은 토마토가 모두 익을 때까지 최소 며칠이 걸리는지를 계산해서 출력해야 한다.

만약 저장될 때부터 모든 토마토가 익어있는 상태이면 0을 출력해야하고

토마토가 모두 익지는 못하는 상황이면 -1을 출력해야 한다.

---

## 💻 예제

### 예제 입력 1

```plain text

```

### 예제 출력 1

```plain text

```

---

## ✏️ 풀이

```python
# 1트 성공, 1시간
import sys
from collections import deque
input = sys.stdin.readline

m, n, h = map(int, input().rstrip().split())

# print(m, n, h)

boxes, visited = {}, {}
for i in range(h):
    box = []
    visit = []
    for j in range(n):
        col = list(map(int, input().rstrip().split()))
        box.append(col)
        visit.append([False] * len(col))

    boxes[i] = box
    visited[i] = visit

# print(boxes)
# print(visited)

def bfs():
    # push initial values into queue
    queue = deque()
    for l in range(h):
        box = boxes[l]
        for i in range(len(box)):
            for j in range(len(box[i])):
                if box[i][j] == 1:
                    queue.append((i, j, l, 0))
                    boxes[l][i][j] = 1
                    visited[l][i][j] = True

    while queue:
        cur_x, cur_y, cur_l, cur_cnt = queue.popleft()

        # same layer
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]

            cur_box = boxes[cur_l]
            cur_visited = visited[cur_l]
            if 0 <= nx < n and 0 <= ny < m:
                if cur_box[nx][ny] == 0 and not cur_visited[nx][ny]:
                    queue.append((nx, ny, cur_l, cur_cnt+1))
                    boxes[cur_l][nx][ny] = 1
                    visited[cur_l][nx][ny] = True
    
        # different layers: up & down
        dl = [1, -1]
        for i in range(2):
            nl = cur_l + dl[i]

            if 0 <= nl < h:
                cur_box = boxes[nl]
                cur_visited = visited[nl]
                if 0 <= cur_x < n and 0 <= cur_y < m:
                    if cur_box[cur_x][cur_y] == 0 and not cur_visited[cur_x][cur_y]:
                        queue.append((cur_x, cur_y, nl, cur_cnt+1))
                        boxes[nl][cur_x][cur_y] = 1
                        visited[nl][cur_x][cur_y] = True
    
    return cur_cnt

flag = False
for l in boxes:
    box = boxes[l]
    for i in range(len(box)):
        for j in range(len(box[i])):
            if box[i][j] == 0:
                flag = True
                break

if flag:
    cnt = bfs()

    flag2 = False
    n_tomato = 0
    for l in boxes:
        box = boxes[l]
        for i in range(len(box)):
            for j in range(len(box[i])):
                if box[i][j] == 1:
                    n_tomato += 1
                if box[i][j] == 0:
                    flag2 = True
                    break

    if flag2:
        print(-1)
    else:
        print(cnt)

else:
    print(0)
```


