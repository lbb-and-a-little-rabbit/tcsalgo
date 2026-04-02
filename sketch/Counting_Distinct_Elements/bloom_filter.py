from lib_hash import bloom_hash
from bitarray import bitarray
from pympler import asizeof

def bloom_filter(textname: str, k: int = 7, m: int = 3840000) -> bitarray :
    bit_arr = bitarray(m)
    bit_arr.setall(0)
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                for i in range(k) :
                    idx = bloom_hash(word, i, m)
                    bit_arr[idx] = 1
    
    return bit_arr

def query(bit_arr: bitarray, set: set, k = 7, m = 3840000) :
    while (True) :
        q = input()
        if q == "quit" :
            return       
        print(f"{q} 在文本中" if q in set else f"{q} 不在文本中")
        flag = True
        for i in range(k) :
            if bit_arr[bloom_hash(q, i, m)] == 0 :
                flag = False
                break
        print(f"预测{q} 在文本中" if flag else f"预测{q} 不在文本中")

set = set()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            if word not in set :
                set.add(word)
        
ba = bloom_filter("test_data.txt")

print(f"set 所占内存 {asizeof.asizeof(set)} 字节")
print(f"bitarr所占内存 {asizeof.asizeof(ba)} 字节")

query(ba, set)

class CBF:
    def __init__(self):
        self.m = 3840000 # bytesit位次
        self.k = 7  # 哈希函数数量
        self.byte_arr = bytearray(self.m)

    def insert(self, word: str) :
        for i in range(self.k) :
            idx = bloom_hash(word, i, self.m)
            if self.byte_arr[idx] < 255 :
                self.byte_arr[idx] += 1
    
    def delete(self, word: str) :
        if not self.query(word, False) :
            return
        for i in range(self.k) :
            idx = bloom_hash(word, i, self.m)
            if self.byte_arr[idx] > 0 :
                self.byte_arr[idx] -= 1
    
    def query(self, word: str, isPrint = True) -> bool:
        for i in range(self.k) :
            idx = bloom_hash(word, i, self.m)
            if self.byte_arr[idx] == 0 :
                print(f"{word} 不在文本中")
                return False
        print(f"{word} 大概率在文本中")
        return True