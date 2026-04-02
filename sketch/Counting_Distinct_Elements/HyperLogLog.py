from lib_hash import get_hll_params_custom

def HLL(textname: str,b: int) -> float :
    m = 2 ** b
    map = [0] * m
    with open(textname, "r") as f :
        for line in f :
            for word in line.split() :
                idx, rho = get_hll_params_custom(word, b)
                map[idx] = max(map[idx], rho)

    if m == 16:
        alpha_m = 0.673
    elif m == 32:
        alpha_m = 0.697
    elif m == 64:
        alpha_m = 0.709
    else:
        alpha_m = 0.7213 / (1 + 1.079 / m)

    val = alpha_m * m * m / sum(1 / 2 ** map[i] for i in range(m))
    return val

word_set = set()
with open("test_data.txt", "r") as f :
    for line in f :
        for word in line.split() :
            word_set.add(word)

print(f"真实的去重词数 (F0): {len(word_set)}")

print(f"HyperLogLog Algorithm 估算去重词数(F1): {HLL('test_data.txt', 10)}")