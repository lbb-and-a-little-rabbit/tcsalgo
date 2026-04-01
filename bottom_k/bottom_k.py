from hash01 import hash_to_01
from maxheap import MaxHeap

word_set = set()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            word_set.add(word)

print(f"真实的去重词数 (F0): {len(word_set)}")

k = 3000
seen_set = set()
maxheap = MaxHeap()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            hash = hash_to_01(word)
            if len(maxheap) < k and hash not in seen_set:
                maxheap.push(hash)
                seen_set.add(hash)
            else :
                if maxheap.peek() > hash and hash not in seen_set:
                    top = maxheap.pop()
                    seen_set.remove(top)
                    maxheap.push(hash)
                    seen_set.add(hash)

print(f"Bottom_k Algorithm 估算去重次数(F1): {k / maxheap.peek()}")