def gethash(x, m: int):
    h = hash(x)
    h1 = h % m
    h2 = (h >> 16 | h << 16) % m
    return h1, h2

class p2c:
    def __init__(self, m: int):
        self.m = m
        self.list = [[] for _ in range(m)]

    # 不考虑重复插入
    def insert(self, x):
        h1, h2 = gethash(x, self.m)
        n1 = len(self.list[h1])
        n2 = len(self.list[h2])
        if n1 <= n2:
            if x not in self.list[h1]:
                self.list[h1].append(x)
        else:
            if x not in self.list[h2]:
                self.list[h2].append(x)

    def delete(self, x):
        h1, h2 = gethash(x, self.m)
        if x in self.list[h1]:
            self.list[h1].remove(x)
        if x in self.list[h2]:
            self.list[h2].remove(x)
        
    def find(self, x):
        h1, h2 = gethash(x, self.m)
        if x in self.list[h1]:
            return True
        if x in self.list[h2]:
            return True
        return False