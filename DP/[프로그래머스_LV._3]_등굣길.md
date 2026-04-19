# [프로그래머스 LV. 3] 등굣길

---

# 문제 설명

---

# 풀이 (50분 소요)

> 오랜만에 풀어서 시간은 좀 소요됐지만 문제 난이도 자체는 크게 어렵지 않았던 것 같다. 이제 LV.4로 넘어가도 될 것 같다.

```python
def solution(m, n, puddles):
    MOD = 1000000007
    
    dp = [[0] * m for _ in range(n)]
    
    for x, y in puddles:
        dp[y-1][x-1] = -1
    
    dp[0][0] = 1
    
    for i in range(n):
        for j in range(m):
            if dp[i][j] == -1:
                dp[i][j] = 0
                continue
            
            if i == 0 and j == 0:
                continue
            
            up = dp[i-1][j] if i > 0 else 0
            left = dp[i][j-1] if j > 0 else 0
            
            dp[i][j] = (up + left)
    
    return dp[n-1][m-1] % MOD
```


