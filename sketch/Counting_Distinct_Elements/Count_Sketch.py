from lib_hash import min_sketch_hash, g_sketch_hash
import statistics
from pympler import asizeof

def Count_Sketch(textname: str, hash_cnt: int, w: int, begin_seed = 0) -> list :
    map = [[0] * w for _ in range(hash_cnt)]
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                for i in range(hash_cnt) :
                    h = min_sketch_hash(word, i + begin_seed, w)
                    g = g_sketch_hash(word, i + begin_seed + 10000)
                    map[i][h] += g
    
    return map

dict = {}
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            if word not in dict :
                dict[word] = 1
            else :
                dict[word] += 1

dict_size = asizeof.asizeof(dict)
hc = 5
width = 2000
map = Count_Sketch("test_data.txt", hc, width)
map_size = asizeof.asizeof(map)

print(f"dict所占内存: {dict_size} 字节")
print(f"map所占内存: {map_size} 字节")

while (True) :
    print("输入查询词:")
    query = input()
    if query == "quit" :
        break
    if query in dict:
        print(f"{query} 实际出现次数: {dict[query]}")
    else :
        print(f"{query} 实际出现次数: 0")
    v = []
    for i in range(hc) :
        h = min_sketch_hash(query, i, width)
        g = g_sketch_hash(query, i + 10000)
        v.append(map[i][h] * g)
    res = statistics.median(v)
    print(f"{query} 预估出现次数: {res}")