import os
import re

# 定义文件夹路径
folder_path = "dataForLearning/10000"

# 生成所有预期的文件名模式（仅用于比较n和m）
expected_files = {(n, m) for n in range(101, 501) for m in range(1, 19)}

# 获取文件夹内所有文件名
try:
    existing_files = os.listdir(folder_path)
except FileNotFoundError:
    print("文件夹 '202511' 不存在")
    exit()

# 提取现有文件中的n和m
existing_pairs = set()
for file in existing_files:
    # 使用正则表达式匹配 n-任意字符-m.csv 格式
    match = re.match(r"(\d+)-.*-(\d+)\.csv", file)
    if match:
        n, m = int(match.group(1)), int(match.group(2))
        if 101 <= n <= 500 and 1 <= m <= 18:
            existing_pairs.add((n, m))

# 找出缺失的(n, m)对
missing_pairs = expected_files - existing_pairs

# 转换为文件名格式并排序
missing_files = [f"{n}-*-{m}.csv" for n, m in sorted(missing_pairs, key=lambda x: (x[0], x[1]))]

print("缺失的文件编号：")
for file in missing_files:
    print(file)

# 输出缺失文件总数
print(f"\n总计缺失文件数：{len(missing_files)}")