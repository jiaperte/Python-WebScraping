def minMoves(maze, x, y):
    dp = []
    dp[0] = 0
    for i in range(max(x, y)):
        for j in range(min(x, y)):
            if maze[i][j]
