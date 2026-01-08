# ### Version 1. graph + visited ###
# import sys
# sys.setrecursionlimit(10**6)
# input = sys.stdin.readline

# M, N = map(int, input().split())

# graph = []
# visited = []
# for i in range(M):
#     graph.append(list(map(int, input().split())))
#     visited.append([False] * len(graph[i]))

# def dfs(cur_x, cur_y):
#     # check visited
#     visited[cur_x][cur_y] = True

#     dx = [-1, 0, 1, 0, -1, -1, 1, 1]
#     dy = [0, 1, 0, -1, -1, 1, -1, 1]

#     for i in range(8):
#         nx = cur_x + dx[i]
#         ny = cur_y + dy[i]

#         # check valid direction
#         if 0 <= nx < M and 0 <= ny < N:
#             if graph[nx][ny] and not visited[nx][ny]:
#                 dfs(cur_x=nx, cur_y=ny)
        
# cnt = 0
# for i in range(M):
#     for j in range(N):
#         if graph[i][j] and not visited[i][j]:
#             dfs(i, j)
#             cnt += 1

# print(cnt)

### Version 2. graph ###
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

M, N = map(int, input().split())

graph = []
for i in range(M):
    graph.append(list(map(int, input().split())))

def dfs(cur_x, cur_y):
    # check visited
    graph[cur_x][cur_y] = 0

    dx = [-1, 0, 1, 0, -1, -1, 1, 1]
    dy = [0, 1, 0, -1, -1, 1, -1, 1]

    for i in range(8):
        nx = cur_x + dx[i]
        ny = cur_y + dy[i]

        # check valid direction
        if 0 <= nx < M and 0 <= ny < N:
            if graph[nx][ny]:
                dfs(cur_x=nx, cur_y=ny)
        
cnt = 0
for i in range(M):
    for j in range(N):
        if graph[i][j]:
            dfs(i, j)
            cnt += 1

print(cnt)