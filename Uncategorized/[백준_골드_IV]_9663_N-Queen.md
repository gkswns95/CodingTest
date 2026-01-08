# [백준 골드 IV] 9663: N-Queen

> 🏷️ #브루트포스 알고리즘 | #백트래킹

> 🔗 www.acmicpc.net
https://www.acmicpc.net/problem/9663

---

---

## 📋 문제

N-Queen 문제는 크기가 N × N인 체스판 위에 퀸 N개를 서로 공격할 수 없게 놓는 문제이다.

N이 주어졌을 때, 퀸을 놓는 방법의 수를 구하는 프로그램을 작성하시오.

---

## 📥 입력

첫째 줄에 N이 주어진다. (1 ≤ N < 15)

---

## 📤 출력

첫째 줄에 퀸 N개를 서로 공격할 수 없게 놓는 경우의 수를 출력한다.

---

## 💻 예제

### 예제 입력 1

```plain text
8
```

### 예제 출력 1

```plain text
92
```

---

## ✏️ 풀이

```python
import sys
sys.setrecursionlimit(10**6)

input = sys.stdin.readline

n = int(input())

def dfs(x, y, n_queen):
    if n_queen == n:
        return 1

    ret = 0
    for i in range(n): # col loop
        nx = x + 1
        ny = i

        if nx >= n:
            continue
        
        if not v_col[ny] and not v_diag1[nx+ny] and not v_diag2[nx-ny]:
            v_col[ny] = True
            v_diag1[nx+ny] = True
            v_diag2[nx-ny] = True
            ret += dfs(nx, ny, n_queen+1)
            v_col[ny] = False
            v_diag1[nx+ny] = False
            v_diag2[nx-ny] = False
    
    return ret
    
v_col = [False for _ in range(n)]
v_diag1 = [False for _ in range(2*n-1)]
v_diag2 = [False for _ in range(2*n-1)]

cnt = 0
for i in range(n): # column loop
    v_col[i] = True
    v_diag1[0+i] = True
    v_diag2[0-i] = True
    cnt += dfs(0, i, n_queen=1)
    v_col[i] = False
    v_diag1[0+i] = False
    v_diag2[0-i] = False

print(cnt)
```
