import numpy as np

def perfect_matching(adj: np.array) -> bool:
    n = len(adj)
    edmond = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if adj[i][j]:
                edmond[i][j] = np.random.randint(1, 100000)
    
    return abs(np.linalg.det(edmond)) > 1e-5

# --- 验证实例 ---

# 实例 1: 简单的 2x2 完美匹配 (学生1->项目1, 学生2->项目2)
adj1 = np.array([
    [1, 0],
    [0, 1]
])

# 实例 2: 3x3 环形匹配 (1->2, 2->3, 3->1)
adj2 = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])

# 实例 3: 没有完美匹配 (学生 0 和 1 都只喜欢项目 0，项目 1 没人要)
adj3 = np.array([
    [1, 0],
    [1, 0]
])

# 实例 4: 稍微复杂的 4x4 存在匹配
adj4 = np.array([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
])

print(f"实例 1 (2x2 存在): {perfect_matching(adj1)}")   # 应为 True
print(f"实例 2 (3x3 存在): {perfect_matching(adj2)}")   # 应为 True
print(f"实例 3 (2x2 不存在): {perfect_matching(adj3)}") # 应为 False
print(f"实例 4 (4x4 存在): {perfect_matching(adj4)}")   # 应为 True