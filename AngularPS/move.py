import os
import shutil
import re

# 源目录
src_dir = "./modelD"

# 目标目录
dst_testing = "./dataForTesting/modelD"
dst_validation = "./dataForValidation/modelD"
dst_learning = "./dataForLearning/modelD"

# 确保目标目录存在
for d in [dst_testing, dst_validation, dst_learning]:
    os.makedirs(d, exist_ok=True)

# 正则：匹配文件名开头的 3 位编号
pattern = re.compile(r"^(\d{3}).*\.csv$")

for filename in os.listdir(src_dir):
    match = pattern.match(filename)
    if not match:
        continue

    idx = int(match.group(1))
    src_path = os.path.join(src_dir, filename)

    if 1 <= idx <= 50:
        dst_path = os.path.join(dst_testing, filename)
    elif 51 <= idx <= 100:
        dst_path = os.path.join(dst_validation, filename)
    elif 101 <= idx <= 500:
        dst_path = os.path.join(dst_learning, filename)
    else:
        continue

    shutil.move(src_path, dst_path)
    print(f"Moved {filename} -> {dst_path}")

print("✅ 文件移动完成")
