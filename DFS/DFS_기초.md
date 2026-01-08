# DFS 기초

```python
# 주어진 그래프를 DFS로 탐색한 결과를 출력하는 프로그램을 작성하시오.
# DFS 문제의 세 가지 구성 요소
# 1. Graph
# 2. Visited
# 3. Recursion

graph = {
    1: [2, 3, 4],
    2: [5],
    3: [],
    4: [6],
    5: [],
    6: []
}

# Set visited dictionary using graph keys.
visited = {k: False for k in graph.keys()}

def dfs(cur_node):
   
    if not visited[cur_node]: # check visited
        visited[cur_node] = True

        print(cur_node, end=' ')

        neighbor = graph[cur_node]
        for next_node in neighbor:
            dfs(cur_node=next_node)

dfs(cur_node=1)
print()
```

- Python의 `print()` 함수는 기본적으로 출력이 끝난 뒤 줄바꿈을 자동으로 수행함
- 줄바꿈을 없애기 위해서는 `end=' '` 옵션을 사용할 수 있음