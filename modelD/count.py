import os

folder = "./caseC"

count = sum(
    1 for f in os.listdir(folder)
    if f.lower().endswith(".csv") and os.path.isfile(os.path.join(folder, f))
)

print(f"{folder} 中共有 {count} 个 CSV 文件")
