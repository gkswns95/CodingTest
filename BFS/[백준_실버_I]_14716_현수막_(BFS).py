### Version 1. 시간 초과 (풀이시간: 15분)
import sys
from collections import deque

input = sys.stdin.readline

M, N = map(int, input().split())

graph = []
for i in range(M):
    graph.append(list(map(int, input().split())))

def bfs(x, y):
    queue = deque([(x, y)])

    dx = [-1, 0, 1, 0, -1, -1, 1, 1]
    dy = [0, 1, 0, -1, -1, 1, 1, -1]

    while queue:
        cur_x, cur_y = queue.popleft()
        graph[cur_x][cur_y] = 0 # check visitied
        for i in range(8):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]
            if 0 <= nx < M and 0 <= ny < N:
                if graph[nx][ny]:
                    queue.append((nx, ny))


cnt = 0
for i in range(M):
    for j in range(N):
        if graph[i][j]:
            bfs(i, j)
            cnt += 1

print(cnt)

# ---

### Version 2. 성공
import sys
from collections import deque

input = sys.stdin.readline

M, N = map(int, input().split())

graph = []
for i in range(M):
    graph.append(list(map(int, input().split())))

def bfs(x, y):
    queue = deque([(x, y)])
    graph[x][y] = 0 # check visitied

    dx = [-1, 0, 1, 0, -1, -1, 1, 1]
    dy = [0, 1, 0, -1, -1, 1, 1, -1]

    while queue:
        cur_x, cur_y = queue.popleft()
        for i in range(8):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]
            if 0 <= nx < M and 0 <= ny < N:
                if graph[nx][ny]:
                    graph[nx][ny] = 0 # check visitied
                    queue.append((nx, ny))


cnt = 0
for i in range(M):
    for j in range(N):
        if graph[i][j]:
            bfs(i, j)
            cnt += 1

print(cnt)