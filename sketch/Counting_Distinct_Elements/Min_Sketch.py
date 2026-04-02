from lib_hash import min_sketch_hash
import statistics

def Min_Sketch(textname: str, hash_cnt: int,w: int, words: list, isprint = True, begin_seed = 0) -> list :
    map = [[0] * w for _ in range(hash_cnt)]
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                for i in range(hash_cnt) :
                    map[i][min_sketch_hash(word, i + begin_seed, w)] += 1
    
    res = []
    for word in words :
        cnt = min(map[i][min_sketch_hash(word, i + begin_seed, w)] for i in range(hash_cnt))
        if isprint :
            print(f"{word} 预估出现次数为: {cnt}")
        res.append(cnt)
    
    return res

def median_trick(textname: str, hash_cnt: int,w: int, words: list, L: int) :
    esit = []
    for i in range(L) :
        esit.append(Min_Sketch(textname, hash_cnt, w, words, False, i * hash_cnt))
    

    for i in range(len(words)) :
        word_all_estimates = [esit[copy_idx][i] for copy_idx in range(L)]
        cnt = statistics.median(word_all_estimates)
        print(f"{words[i]} median trick  预估出现次数为: {cnt}")

words = ["192.168.1.11", "192.168.1.6"]
with open("test_data.txt", "r") as f :
    cnt0, cnt1, total_cnt = 0, 0, 0
    for line in f :
        for word in line.split() :
            if word == "192.168.1.11" :
                cnt0 += 1
            if word == "192.168.1.6" :
                cnt1 += 1
            total_cnt += 1

print(f"总词数 : {total_cnt}")
print(f"'192.168.1.11' 出现次数为 {cnt0}")
print(f"'192.168.1.6' 出现次数为 {cnt1}")
tmp = Min_Sketch("test_data.txt", 5, 2000, words)
median_trick("test_data.txt", 5, 2000, words, 20)