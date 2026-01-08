import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

n = int(input())

graph = {}
for i in range(n):
    kv = input().rstrip().split(' ')
    graph[kv[0]] = kv[-1]

def dfs(k, v):
    ret = False
    if k in graph.keys() and graph[k] == v:
        ret = True
    else:
        if k in graph.keys() and graph[k] in graph.keys():
            ret = dfs(k=graph[k], v=v)
    
    return ret

m = int(input())
for i in range(m):
    kv = input().rstrip().split(' ')
    if dfs(k=kv[0], v=kv[-1]):
        print('T')
    else:
        print('F')