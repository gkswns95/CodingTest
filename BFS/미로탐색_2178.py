from collections import deque
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

# print(n, m)

graph, visited = [], []

graph.append([0] * (m+1))
for i in range(n):
    graph.append([0] + list(map(int, input().rstrip())))

for i in range(len(graph)):
    visited.append([False] * len(graph[i]))

# print(graph)

def visualize_graph(graph):
    for i in range(n+1):
        print(graph[i])
    
    print("-" * 20)

def bfs(x, y):
    queue = deque([(x, y)])
    visited[x][y] = True

    while queue:
        cur_x, cur_y = queue.popleft()

        ### debug ###
        # print(f'cur_x: {cur_x}, cur_y: {cur_y}')
        if cur_x == n and cur_y == m:
            break

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            nx = cur_x + dx[i]
            ny = cur_y + dy[i]

            if 0 <= nx < n+1 and 0 <= ny < m+1:
                if not visited[nx][ny] and graph[nx][ny] == 1:
                    queue.append((nx, ny))
                    graph[nx][ny] = graph[cur_x][cur_y] + 1
                    visited[nx][ny] = True

                    ### debug ###
                    # visualize_graph(graph)

bfs(1, 1)
print(graph[n][m])