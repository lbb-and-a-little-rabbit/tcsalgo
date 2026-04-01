import hashlib

def hash_to_01(element, seed=0):
    # 1. 将元素转化为字符串并加上盐值（为了独立性）
    s = str(element) + str(seed)
    
    # 2. 使用 SHA-256 生成哈希（返回的是字节流）
    hash_bytes = hashlib.sha256(s.encode('utf-8')).digest()
    
    # 3. 取前 8 字节并转化为 64 位无符号整数
    # 'big' 表示大端字节序，unsigned long long 最大值是 2^64 - 1
    hash_int = int.from_bytes(hash_bytes[:8], 'big')
    
    # 4. 归一化到 [0, 1]
    return hash_int / (2**64)

# 示例
# print(hash_to_01("apple"))
# print(hash_to_01("banana")) 