import sys
from collections import deque
input = sys.stdin.readline

graph = {}
n = int(input())
for i in range(n):
    k, _, v = input().split()
    graph[k] = v

def bfs(k, v):
    queue = deque([(k, v)])

    while queue:
        k, v = queue.popleft()
        if k in graph:
            if graph[k] == v:
                return True
            else:
                for neighbor in list(graph[k]):
                    if graph[k] in graph:
                        queue.append((graph[k], v))
        else:
            return False
    
    return False


m = int(input())
for i in range(m):
    k, _, v = input().split()
    if bfs(k, v):
        print('T')
    else:
        print('F')