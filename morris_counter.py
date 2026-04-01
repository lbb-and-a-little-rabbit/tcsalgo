import random

def morris_counter(x: int, a: float) -> int:
    if random.random() < 1 / (1 + a) ** x :
        x += 1
    return x

result = []
k = 100
n = 10 ** 5
a = 0.1  # 0 < a <= 1

for _ in range(k) :
    x = 0

    for i in range(0, n) :
        x = morris_counter(x, a)
    
    result.append((((1 + a) ** x) - 1) / a)

res = sum(result) / k

print("n = ",end = "")
print(n)
print("averge_result = ",end = "")
print(res)