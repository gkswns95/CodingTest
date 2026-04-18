import sys
input = sys.stdin.readline


def solver(n):
    dp = [0] * n
    dp[0], dp[1] = 1, 3
    for i in range(2, n):
        dp[i] = dp[i-1] + dp[i-2] * 2
    
    print(dp[-1])

while True:
    try:
        solver(int(input()))
    except:
        break