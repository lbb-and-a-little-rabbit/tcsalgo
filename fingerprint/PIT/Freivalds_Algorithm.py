import numpy as np
import time

N = 2000
k = 20
flag = True

A = np.random.randint(0, 10000, (N, N))
B = np.random.randint(0, 10000, (N, N))

time0_s = time.time()

C = np.dot(A, B)

time0_e = time.time()

time1_s = time.time()

for i in range(k):
    arr = np.random.randint(0, 1, (N, 1))
    T1 = np.dot(C, arr)
    T2 = np.dot(A, np.dot(B, arr))
    if (T1 != T2).any():
        flag = False
        break

time1_e = time.time()

if flag:
    print(True)

print(f"normal algorithm costs {time0_e - time0_s : .4f} s")
print(f"Freivalds' Algorithm costs {time1_e - time1_s : .4f} s")