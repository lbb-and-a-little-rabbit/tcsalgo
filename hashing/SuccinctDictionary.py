from bitarray import bitarray
import math

class SuccinctDictionary:
    def __init__(self, data_list, universe_size):
        self.u = universe_size
        # 1. 物理层：创建真正的位数组
        self.bv = bitarray(self.u)
        self.bv.setall(0)
        for x in data_list:
            if 0 <= x < self.u:
                self.bv[x] = 1
        
        # 2. 辅助索引层：每 B 位一个 Block
        # 理论上 B 应该取 (log U) / 2，这里取 64 方便计算
        self.block_size = 64
        self.num_blocks = math.ceil(self.u / self.block_size)
        
        # 预计算每个 block 之前 1 的总数
        self.block_ranks = [0] * self.num_blocks
        count = 0
        for i in range(self.num_blocks):
            self.block_ranks[i] = count
            # bitarray 的 .count() 是在 C 层面实现的，极快
            start = i * self.block_size
            end = min(start + self.block_size, self.u)
            count += self.bv[start:end].count(1)
        self.total_ones = count

    def exists(self, x):
        """查询元素是否存在: O(1)"""
        return self.bv[x] if 0 <= x < self.u else False

    def rank(self, i):
        """计算 [0, i] 中 1 的个数 (核心简洁运算): O(1)"""
        if i < 0: return 0
        if i >= self.u: i = self.u - 1
        
        block_idx = i // self.block_size
        start_of_block = block_idx * self.block_size
        
        # 基础值 + 块内局部扫描
        # bitarray 切片和 count 依然是 $O(1)$ 的逻辑速度（由底层优化保证）
        return self.block_ranks[block_idx] + self.bv[start_of_block : i + 1].count(1)
    
    def select(self, k):
        """查询第 k 个 1 出现的位置 (k 从 1 开始)"""
        if k < 1 or k > self.total_ones:
            return None
        
        # 1. 块级粗定位：在 block_ranks 中二分查找
        # 找到最大的 block_idx 使得 block_ranks[block_idx] < k
        low = 0
        high = len(self.block_ranks) - 1
        best_block = 0
        while low <= high:
            mid = (low + high) // 2
            if self.block_ranks[mid] < k:
                best_block = mid
                low = mid + 1
            else:
                high = mid - 1
        
        # 2. 块内精确定位
        # 计算在当前块内还需要找多少个 1
        needed = k - self.block_ranks[best_block]
        start_pos = best_block * self.block_size
        
        # 利用 bitarray 的高效 index 方法查找块内第 needed 个 1
        # .index(value, start, stop)
        count = 0
        pos = start_pos - 1
        for _ in range(needed):
            # 找到下一个 1 的位置
            pos = self.bv.index(1, pos + 1)
        return pos
    
    