import random

# 2-元独立

class two_wise_Independent_hashings_family:
    def __init__(self, m: int, seed = 114514, p = 10 ** 9 + 7):
        self.m = m
        self.p = p
        random.seed(seed)
        self.a = random.randint(1, p - 1)
        self.b = random.randint(0, p - 1)

    def gethash(self, x) -> int :
        a = self.a
        b = self.b
        m = self.m
        p = self.p
        val = hash(x)
        return ((a * val + b) % p) % m  
        # 3-元独立：$$h(x) = ((ax^2 + bx + c) \pmod p) \mod m$$  k-元独立增加多项式次数即可