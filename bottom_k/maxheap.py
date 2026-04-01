import heapq

class MaxHeap:
    """最大堆实现"""
    
    def __init__(self):
        self.heap = []
    
    def push(self, value):
        heapq.heappush(self.heap, -value)
    
    def pop(self):
        if self.heap:
            return -heapq.heappop(self.heap)
        raise IndexError("pop from empty heap")
    
    def peek(self):
        if self.heap:
            return -self.heap[0]
        raise IndexError("peek from empty heap")
    
    def __len__(self):
        return len(self.heap)
    
    def __bool__(self):
        return bool(self.heap)

# 使用示例
# max_heap = MaxHeap()
# max_heap.push(5)
# max_heap.push(2)
# max_heap.push(8)
# max_heap.push(1)

# print(f"最大值: {max_heap.peek()}")  # 8
# print(f"弹出最大值: {max_heap.pop()}")  # 8
# print(f"下一个最大值: {max_heap.peek()}")  # 5