# 仅限于静态数据集
import random

def str_to_int(s, base, p):
    h = 0
    for char in s:
        h = (h * base + ord(char)) % p
    return h

class FKS_str:
    def __init__(self, S: list[str]):
        self.p = (1 << 61) - 1  # 梅森素数
        self.base = 257         # 多项式基数
        self.n = len(S)
        self.m = self.n
        raw_data = S
        int_data = [str_to_int(s, self.base, self.p) for s in S]

        # 一级构建
        while True:
            self.bucket = [[] for _ in range(self.m)] 
            self.bucket_raw = [[] for _ in range(self.m)]
            self.a = random.randint(1, self.p - 1)
            self.b = random.randint(0, self.p - 1)
            for i, val in enumerate(int_data):
                idx = ((self.a * val + self.b) % self.p) % self.m
                self.bucket[idx].append(val)
                self.bucket_raw[idx].append(raw_data[i])
            if sum(len(b) ** 2 for b in self.bucket) < 2 * self.n:
                break
        
        # 二级构建
        self.tables = [None] * self.m
        for i in range(self.m):
            if not self.bucket[i]:
                continue

            while True:
                a_i = random.randint(1, self.p - 1)
                b_i = random.randint(0, self.p - 1)
                m_i = len(self.bucket[i]) ** 2
                data = [None] * m_i
                collision = False
                for j, val in enumerate(self.bucket[i]):
                    idx = ((a_i * val + b_i) % self.p) % m_i
                    if data[idx] is None:
                        data[idx] = self.bucket_raw[i][j]
                    else:
                        collision = True
                        break
                if not collision:
                    self.tables[i] = (a_i, b_i, m_i, data)
                    break
        self.bucket = None
        self.bucket_raw = None

    def find(self, s: str) -> bool:
        val = str_to_int(s, self.base, self.p)
        idx1 = ((self.a * val + self.b) % self.p) % self.m
        if self.tables[idx1] == None:
            return False
        a, b, m, data = self.tables[idx1]
        idx2 = ((a * val + b) % self.p) % m 
        return s == data[idx2]