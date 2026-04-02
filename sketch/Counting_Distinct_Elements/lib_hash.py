import hashlib

def hash_to_01(element, seed = 0):
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

def rho_fm_hash(element, seed=0):
    """
    计算元素哈希值末尾连续 0 的个数 (Trailing Zeros)
    """
    # 1. 将元素和种子结合（为了实现多副本独立哈希）
    s = str(element) + str(seed)
    
    # 2. 生成 MD5 哈希（128位），并转为大整数
    h_hex = hashlib.md5(s.encode('utf-8')).hexdigest()
    h_int = int(h_hex, 16)
    
    # 3. 计算末尾连续 0 的个数
    if h_int == 0:
        return 128  # 特殊情况：全 0
        
    count = 0
    # 只要最后一位是 0，就右移一位并计数
    while h_int & 1 == 0:
        count += 1
        h_int >>= 1
        
    return count

def min_sketch_hash(element, seed, width):
    """
    将元素映射到 [0, width-1] 之间的整数桶
    :param element: 输入的单词或数据
    :param seed: 种子（对应 Min-Sketch 的第几行）
    :param width: 数组的宽度 (w)
    """
    # 1. 结合元素和种子，确保每一行的哈希函数是独立的
    s = str(element) + str(seed)
    
    # 2. 使用 MD5 生成 128 位哈希值
    h_hex = hashlib.md5(s.encode('utf-8')).hexdigest()
    
    # 3. 转为整数并对宽度取模
    h_int = int(h_hex, 16)
    return h_int % width

def g_sketch_hash(element, seed = 0):
    """
    g(x) -> {+1, -1}
    """
    s = str(element) + str(seed) + "sign" # 加个后缀防止与 h(x) 冲突
    h_hex = hashlib.md5(s.encode('utf-8')).hexdigest()
    h_int = int(h_hex, 16)
    
    # 偶数返回 1，奇数返回 -1
    return 1 if h_int % 2 == 0 else -1