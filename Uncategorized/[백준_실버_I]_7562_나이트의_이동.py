from collections import deque
import sys
input = sys.stdin.readline

n_cases = int(input())

# print(f'n_cases: {n_cases}')

def visualize_graph(graph):
    for i in range(len(graph[0])):
        print(graph[i])
    
    print()

def bfs(sx, sy, ex, ey):
    queue = deque([(sx, sy, 0)])
    # check visited
    graph[sx][sy] = True

    while queue:
        cur_x, cur_y, cur_cnt = queue.popleft()

        # print(f'cur_x: {cur_x}, cur_y: {cur_y}')

        if cur_x == ex and cur_y == ey:
            break
        
        dx = [-2, -1, 1, 2, 2, 1, -1, -2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]

        for i in range(8):
            n_x = cur_x + dx[i]
            n_y = cur_y + dy[i]

            if 0 <= n_x < l and 0 <= n_y < l:
                if not graph[n_x][n_y]:
                    # check visited
                    graph[n_x][n_y] = True    
                    queue.append((n_x, n_y, cur_cnt+1))

    print(cur_cnt)

# Main loop
for i in range(n_cases):
    # Create graph
    l = int(input())
    graph = []
    for i in range(l):
        graph.append([False] * l)

    # Get strat and end points
    s_x, s_y = map(int, input().split())
    e_x, e_y = map(int, input().split())

    # print(f's_x: {s_x}, s_y: {s_y}')
    # print(f'e_x: {e_x}, e_y: {e_y}')

    bfs(s_x, s_y, e_x, e_y)