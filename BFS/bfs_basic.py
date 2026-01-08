from collections import deque

graph = {
    1: [2, 3, 4],
    2: [5],
    3: [],
    4: [6],
    5: [],
    6: []
}

visited = {v: False for v in graph}

def bfs(graph, start):
    queue = deque([start])
    visited[start] = True

    while queue:
        v = queue.popleft()

        print(v, end=' ')

        for neighbor in graph[v]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True


bfs(graph, 1)