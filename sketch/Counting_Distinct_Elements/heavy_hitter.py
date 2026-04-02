from lib_hash import min_sketch_hash, g_sketch_hash
import json
import statistics

def process_text_to_ids(file_path):
    word_to_id = {}
    id_to_word = {}
    content_as_ids = []
    current_id = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.split()
                line_ids = []
                for word in words:
                    # 如果单词不在对照表中，分配一个新 ID
                    if word not in word_to_id:
                        word_to_id[word] = current_id
                        id_to_word[current_id] = word
                        current_id += 1
                    
                    line_ids.append(word_to_id[word])
                
                content_as_ids.append(line_ids)

        # 将对照表保存为 JSON 文件，方便后续查看或恢复
        with open('word_map.json', 'w', encoding='utf-8') as f_map:
            json.dump(word_to_id, f_map, ensure_ascii=False, indent=4)
        
        return content_as_ids, word_to_id, id_to_word

    except FileNotFoundError:
        print("错误：找不到文件，请检查路径。")
        return None

# ids_result为文本字符串转成数字的结果列表， w2i, i2w为两者的对照表
ids_result, w2i, i2w = process_text_to_ids('test_data.txt')

N = 400000
threshold = 2000
total_bits = 13
hash_cnt = 5
width = 2000

# sketches[i] 表示第i层所有前缀;以Count_Sketch算法为例sketches结构为[level][hash_idx][width]
sketches = [[[0] * width for _ in range(hash_cnt)] for _ in range(total_bits + 1)]

# Sketches 构建
for line in ids_result:
    for word_id in line:
        for level in range(total_bits + 1):
            prefix = word_id >> (total_bits - level)
            p_key = f"{level}:{prefix}" # 转字符串为哈希算法实现问题
            for i in range(hash_cnt):
                h = min_sketch_hash(p_key, i, width)
                g = g_sketch_hash(p_key, i + 10000)
                sketches[level][i][h] += g

def query_point(sketches_prefix: list, prefix: int, level: int) :
    # 获得对应前缀prefix的出现频率，可应用Count_Sketch算法的询问部分
    v = []
    pstr = f"{level}:{prefix}"
    for i in range(hash_cnt) :
        h = min_sketch_hash(pstr, i, width)
        g = g_sketch_hash(pstr, seed = i + 10000)
        v.append(sketches_prefix[i][h] * g)

    return statistics.median(v)

def find_heavy_hitter(level: int, prefix: int, total_bits: int = 13) -> list :
    # point query查询某前缀估计频率
    freq = query_point(sketches[level], prefix, level)

    # 该前缀频率小于阈值，heavy_hitter不可能在这个分支，直接剪枝舍弃
    if freq < threshold :
        return []
    
    # 叶子节点，直接返回，为1个符合要求的heavy_hitter
    elif level == total_bits :
        return [prefix]
    
    else :
        res = []
        # 左子树
        res += find_heavy_hitter(level + 1, prefix << 1, total_bits)
        # 右子树
        res += find_heavy_hitter(level + 1, (prefix << 1) + 1, total_bits)
        return res
    
heavy_hitter = find_heavy_hitter(0, 0)
heavy_words = [i2w[heavy_hitter[i]] for i in range(len(heavy_hitter))]
print("算法获值:")
print(heavy_words)

# 准确率评估对比
true_heavy_hitter = []
word_map = {}
with open("test_data.txt", "r") as f:
    for line in f :
        for word in line.split() :
            if word not in word_map:
                word_map[word] = 1
            else:
                word_map[word] += 1
            if word_map[word] >= 2000:
                true_heavy_hitter.append(word)
                word_map[word] -= N

print("真实值:")
print(true_heavy_hitter)