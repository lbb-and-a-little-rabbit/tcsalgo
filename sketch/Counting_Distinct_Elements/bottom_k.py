from lib_hash import hash_to_01
from maxheap import MaxHeap
import statistics

def bottom_k(textname: str, seed = 0, k = 3000) -> float :
    seen_set = set()
    maxheap = MaxHeap()
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                hash = hash_to_01(word, seed)
                if len(maxheap) < k and hash not in seen_set:
                    maxheap.push(hash)
                    seen_set.add(hash)
                else :
                    if maxheap.peek() > hash and hash not in seen_set:
                        top = maxheap.pop()
                        seen_set.remove(top)
                        maxheap.push(hash)
                        seen_set.add(hash)

    return k / maxheap.peek()

def median_trick(textname: str, seed_cnt: int) -> float :
    esti = []
    for i in range(seed_cnt) :
        esti.append(bottom_k(textname, i))
    
    return statistics.median(esti)

word_set = set()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            word_set.add(word)

print(f"真实的去重词数 (F0): {len(word_set)}")

print(f"Bottom_k Algorithm 估算去重次数(F1): {bottom_k('test_data.txt')}")

print(f"Bottom_k Algorithm mediaan trick 估算去重次数(F2): {median_trick('test_data.txt', 20)}")