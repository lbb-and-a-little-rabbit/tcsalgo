class hashing_with_chaining_set:
    def __init__(self, k: int, threshold: float = 0.75):
        self.threshold = threshold
        self.k = k
        self.n = 0
        self.l = [[] for _ in range(k)]

    # 此处没有使用头插法
    def insert_without_check(self, x):
        idx = hash(x) % self.k
        if x in self.l[idx]:
            return
        self.l[idx].append(x)
        self.n += 1

    def rehash(self):
        oldl = self.l
        self.k *= 2
        self.l = [[] for _ in range(self.k)]
        self.n = 0
        for bucket in oldl:
            for element in bucket:
                self.insert_without_check(element)

    def insert(self, x):
        if self.n / self.k >= self.threshold:
            self.rehash()
        
        self.insert_without_check(x)

    def find(self, x) -> bool:
        idx = hash(x) % self.k
        return x in self.l[idx]
    
    def delete(self, x):
        idx = hash(x) % self.k
        if x in self.l[idx]:
            self.l[idx].remove(x)
            self.n -= 1

class hashing_with_chaining_map:
    def __init__(self, k: int, threshold: float = 0.75):
        self.threshold = threshold
        self.k = k
        self.n = 0
        # 每个桶现在存储的是 [key, value] 列表
        self.l = [[] for _ in range(k)]

    def insert_without_check(self, key, value):
        idx = hash(key) % self.k
        # 检查 key 是否已存在，若存在则更新 value（Map 的特性）
        for item in self.l[idx]:
            if item[0] == key:
                item[1] = value
                return
        
        # 若 key 不存在，插入新的键值对 [key, value]
        self.l[idx].append([key, value])
        self.n += 1

    def rehash(self):
        old_l = self.l
        self.k *= 2
        self.l = [[] for _ in range(self.k)]
        self.n = 0
        for bucket in old_l:
            for key, value in bucket:
                self.insert_without_check(key, value)

    def put(self, key, value):
        """对应 C++ 的 map[key] = value 或 insert"""
        if self.n / self.k >= self.threshold:
            self.rehash()
        self.insert_without_check(key, value)

    def get(self, key):
        """对应 C++ 的 map.at(key) 或 find"""
        idx = hash(key) % self.k
        for k, v in self.l[idx]:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def find(self, key) -> bool:
        """检查 key 是否存在"""
        idx = hash(key) % self.k
        for k, v in self.l[idx]:
            if k == key:
                return True
        return False
    
    def delete(self, key):
        idx = hash(key) % self.k
        for i, (k, v) in enumerate(self.l[idx]):
            if k == key:
                self.l[idx].pop(i)
                self.n -= 1
                return True
        return False