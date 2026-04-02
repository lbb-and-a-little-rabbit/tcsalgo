import random

def generate_test_data(filename="test_data.txt", total_lines=100000):
    # 定义一些不同类别的词池，模拟真实世界分布
    ips = [f"192.168.1.{i}" for i in range(1, 101)] # 100个不同IP
    paths = ["/index.html", "/login", "/api/v1/user", "/assets/logo.png", "/search", "/favicon.ico"]
    status_codes = ["200", "404", "500", "302"]
    
    # 随机生成一些唯一的识别码（模拟海量不同用户）
    unique_user_ids = [f"user_{i:05d}" for i in range(5000)] # 5000个不同用户
    
    # 真实的不同词数近似为：100 + 6 + 4 + 5000 = 5110 个左右
    
    with open(filename, "w") as f:
        for _ in range(total_lines):
            ip = random.choice(ips)
            path = random.choice(paths)
            status = random.choice(status_codes)
            user = random.choice(unique_user_ids)
            
            # 每行包含几个词，Bottom-k 将对这些词进行去重统计
            line = f"{ip} {user} {path} {status}\n"
            f.write(line)

generate_test_data()
print("生成完毕！文件名为 test_data.txt")