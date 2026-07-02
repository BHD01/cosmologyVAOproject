import os
import shutil

src_root = "./caseC2"
dst_dir = "./caseC"

# 如果目标目录不存在就创建
os.makedirs(dst_dir, exist_ok=True)

for root, dirs, files in os.walk(src_root):
    for file in files:
        if file.lower().endswith(".csv"):
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_dir, file)

            # 如果目标中已有同名文件，可选择覆盖或跳过
            if os.path.exists(dst_path):
                print(f"跳过（已存在）：{dst_path}")
                continue

            shutil.move(src_path, dst_path)
            print(f"移动：{src_path} -> {dst_path}")
