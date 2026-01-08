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