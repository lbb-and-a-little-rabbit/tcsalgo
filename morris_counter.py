import random

def morris_counter(x: int) -> int:
    if random.random() < 1 / 2 ** x :
        x += 1
    return x

result = []
k = 100
n = 10 ** 5

for _ in range(k) :
    x = 0

    for i in range(0, n) :
        x = morris_counter(x)
    
    result.append(2 ** x - 1)

res = sum(result) / k

print("n = ",end = "")
print(n)
print("averge_result = ",end = "")
print(res)