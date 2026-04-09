import numpy as np

# 从列表创建
a = np.array([1, 2, 3]) 

# 创建全 0 矩阵 (3行4列)
zeros = np.zeros((3, 4))

# 创建等差数列 (0 到 10，步长为 2)
range_arr = np.arange(0, 10, 2)

arr = np.array([1, 2, 3])

print(a)
print(zeros)
print(range_arr)

print(arr + 10)  # [11, 12, 13]
print(arr * 2)   # [2, 4, 6]
print(arr ** 2)  # [1, 4, 9]

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 提取第 1 行
print(arr[0, :]) 

# 提取中间的 2x2 子矩阵
print(arr[0:2, 0:2])

matrix1 = np.random.rand(3, 3)
matrix2 = np.random.randint(0, 1000, (3, 3))

print(matrix1)
print(matrix2)