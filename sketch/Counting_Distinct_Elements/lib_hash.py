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

def get_hll_params_custom(element, b=10):
    """
    不用 mmh3 的 HLL 哈希处理函数
    :param element: 待处理的元素（字符串、数字等）
    :param b: 桶位宽，桶数 m = 2^b
    :return: (index, rho) -> 桶索引, 后导零数量+1
    """
    # 1. 使用 SHA-256 生成哈希，并转为 64 位无符号整数
    # SHA-256 返回 256 位，我们取前 16 位 16 进制字符（即 64 位）
    h_hex = hashlib.sha256(str(element).encode('utf-8')).hexdigest()
    val = int(h_hex[:16], 16)
    
    # 2. 提取桶索引 (取高 b 位)
    index = val >> (64 - b)
    
    # 3. 提取剩余位用于计算后导零
    # 剩余位是通过掩码去掉高 b 位后的值
    remaining_val = val & ((1 << (64 - b)) - 1)
    
    # 4. 计算后导零数量 (Trailing Zeros)
    # rho 的定义通常是：从最低位起第一个 '1' 出现的位置
    # 例如：...1000 -> rho = 4; ...0001 -> rho = 1
    if remaining_val == 0:
        # 如果剩余位全是 0，返回理论最大长度
        rho = 64 - b + 1
    else:
        # 使用位运算技巧：(remaining_val & -remaining_val) 可以提取出最低位的 1
        # 然后用 bit_length() 算出它是第几位
        low_bit = remaining_val & -remaining_val
        rho = low_bit.bit_length()
        
    return index, rho

def bloom_hash(element, seed, m):
    """
    element: 要哈希的元素
    seed: 种子，用于区分不同的哈希函数 (0, 1, 2... k-1)
    m: 位数组的长度
    """
    # 将元素和种子组合，确保每个 seed 产生不同的哈希值
    s = str(element) + str(seed)
    # 使用 MD5 并取模
    hash_val = int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
    return hash_val % m