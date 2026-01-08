# Version 1
# import sys
# sys.setrecursionlimit(10**6)
# input = sys.stdin.readline

# n = int(input())

# graph = {}
# for i in range(n):
#     kv = input().rstrip().split(' ')
#     graph[kv[0]] = kv[-1]

# def dfs(k, v):
#     ret = False
#     if k in graph.keys() and graph[k] == v:
#         ret = True
#     else:
#         if k in graph.keys() and graph[k] in graph.keys():
#             ret = dfs(k=graph[k], v=v)
    
#     return ret

# m = int(input())
# for i in range(m):
#     kv = input().rstrip().split(' ')
#     if dfs(k=kv[0], v=kv[-1]):
#         print('T')
#     else:
#         print('F')

### Version 2
n = int(input())

graph = {}
for _ in range(n):
    k, _, v = input().split()
    graph[k] = v

def dfs(cur_k, v):
    visited[ord(cur_k) - ord('a')] = True
    if cur_k == v:
        return True
    else: 
        if cur_k in graph:
            if not visited[ord(graph[cur_k]) - ord('a')]:
                if dfs(graph[cur_k], v):
                    return True
    
    return False 

m = int(input())
for _ in range(m):
    k, _, v = input().split()
    visited = [False] * 26
    if dfs(k, v):
        print('T')
    else:
        print('F')