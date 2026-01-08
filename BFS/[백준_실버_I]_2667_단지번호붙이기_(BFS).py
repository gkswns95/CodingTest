import sys
from collections import deque

input = sys.stdin.readline

N = int(input())

graph = []
for i in range(N):
    col = list(map(int, input().rstrip()))
    graph.append(col)

# print(graph)

def bfs(x, y):
    cnt = 1
    graph[x][y] = 0

    queue = deque([(x, y)])
    while queue:
        cur_x, cur_y = queue.popleft()

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]

            if 0 <= nx < N and 0 <= ny < N:
                if graph[nx][ny]:
                    queue.append((nx, ny))
                    graph[nx][ny] = 0
                    cnt += 1
    
    return cnt

cnt_list = []
for i in range(N):
    for j in range(N):
        if graph[i][j]:
            cnt_list.append(bfs(i, j))

print(len(cnt_list))
for c in sorted(cnt_list):
    print(c)