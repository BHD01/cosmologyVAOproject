import os
import re

# 重命名21cmvFAST生成的功率谱数据，改为“LW辐射强度_恒星形成率_X射线强度_红移.txt”
# 要求程序所在路径内有dataForLearning（保存功率谱）和Parameter（保存天体物理参数文档）文件夹

def extract_float_from_line(line):
    """提取行中的浮点数"""
    match = re.search(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?", line)
    return match.group() if match else None

def rename_files(base_dir):
    for n in range(5):  # 遍历 LW0 到 LW4 文件夹
        data_path = os.path.join(base_dir, f"dataForLearning/202505/LW{n}")
        param_path = os.path.join(base_dir, f"Parameter/V0L{n}")
        
        if not os.path.exists(data_path) or not os.path.exists(param_path):
            continue
        
        for file in os.listdir(data_path):
            if file.endswith(".txt"):
                parts = file.split("_")
                if len(parts) < 4:
                    continue
                x_old, y_old, z = parts[2], parts[3], parts[4][:-4]  # 获取 x, y, z 值
                walker_file = os.path.join(param_path, f"Walker_{x_old}_1.000000.txt")
                
                if not os.path.exists(walker_file):
                    print(f"文件不存在: {walker_file}")
                    continue
                
                with open(walker_file, "r") as f:
                    lines = f.readlines()
                    if len(lines) < 14:
                        print(f"文件行数不足: {walker_file}")
                        continue
                    x_new = extract_float_from_line(lines[13])  # 第14行
                    y_new = extract_float_from_line(lines[5])   # 第6行
                
                if not x_new or not y_new:
                    print(f"无法提取 x 或 y: {walker_file}")
                    continue
                
                new_filename = f"{n}_{x_new}_{y_new}_{z}.txt"
                old_filepath = os.path.join(data_path, file)
                new_filepath = os.path.join(data_path, new_filename)
                
                os.rename(old_filepath, new_filepath)
                print(f"重命名: {file} -> {new_filename}")

base_directory = "."  # 根目录
rename_files(base_directory)
