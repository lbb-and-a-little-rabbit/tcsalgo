import random

def str_to_int(s, base, p):
    h = 0
    for char in s:
        h = (h * base + ord(char)) % p
    return h

class CuckooHash:
    def __init__(self, m: int, max_kick = 50):
        self.max_kick = max_kick
        self.p = 10 ** 9 + 7
        self.base = 257
        self.m = m
        self.a = [random.randint(1, self.p - 1) for _ in range(2)] 
        self.b = [random.randint(0, self.p - 1) for _ in range(2)]  
        self.t1 = [None] * m
        self.t2 = [None] * m

    def insert(self, s: str):
        # 如果已经存在，直接返回
        if self.find(s):
            return
        
        curr_val = str_to_int(s, self.base, self.p)
        curr_s = s
        
        for _ in range(self.max_kick):
            # 1. 尝试放入第一个表 T1
            idx1 = ((self.a[0] * curr_val + self.b[0]) % self.p) % self.m
            if self.t1[idx1] is None:
                self.t1[idx1] = curr_s
                return
            
            # 2. T1 位置被占，踢出原元素，换 curr_s 进去
            curr_s, self.t1[idx1] = self.t1[idx1], curr_s
            curr_val = str_to_int(curr_s, self.base, self.p) # 更新被踢出元素的 hash 值
            
            # 3. 被踢出的元素尝试去第二个表 T2
            idx2 = ((self.a[1] * curr_val + self.b[1]) % self.p) % self.m
            if self.t2[idx2] is None:
                self.t2[idx2] = curr_s
                return
            
            # 4. T2 位置也被占，再次踢出，换 curr_s 进去
            curr_s, self.t2[idx2] = self.t2[idx2], curr_s
            curr_val = str_to_int(curr_s, self.base, self.p)
            
        # 如果循环结束还没找到位置，说明触发了环路（Cycle）或表太满了
        self.rehash()
        self.insert(curr_s)
            
    def find(self, s: str) -> bool:
        val = str_to_int(s, self.base, self.p)
        idx1 = ((self.a[0] * val + self.b[0]) % self.p) % self.m
        if self.t1[idx1] == s: return True
        
        idx2 = ((self.a[1] * val + self.b[1]) % self.p) % self.m
        if self.t2[idx2] == s: return True
        
        return False

    def rehash(self):
        # 记录旧数据
        old_elements = [x for x in self.t1 if x] + [x for x in self.t2 if x]
        # 扩容并重新选择哈希参数
        self.m *= 2
        self.a = [random.randint(1, self.p - 1) for _ in range(2)]
        self.b = [random.randint(0, self.p - 1) for _ in range(2)]
        self.t1 = [None] * self.m
        self.t2 = [None] * self.m
        
        for x in old_elements:
            self.insert(x)