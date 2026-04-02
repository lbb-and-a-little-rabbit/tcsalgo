from lib_hash import rho_fm_hash
import statistics

def Flajolet_Martin(textname: str, seed = 0) -> float :
    r = 0
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                r = max(r, rho_fm_hash(word, seed))
    
    a = 0.77351
    return 2 ** r / a

def median_trick(textname: str, seed_cnt: int) -> float :
    esti = []
    for i in range(seed_cnt) :
        esti.append(Flajolet_Martin(textname, i))
    
    return statistics.median(esti)

word_set = set()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            word_set.add(word)

print(f"真实的去重词数 (F0): {len(word_set)}")

print(f"Flajolet_Martin Algorithm 估算去重词数(F1): {Flajolet_Martin('test_data.txt')}")

print(f"Flajolet_Martin Algorithm median trick 估算去重词数(F2): {median_trick('test_data.txt', 20)}")