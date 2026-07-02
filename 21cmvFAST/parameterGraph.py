#提取Parameter文件夹内的数据，生成散点图。
# X：恒星形成率    Y：X射线强度

import os
import matplotlib.pyplot as plt


# 存储提取的数据
x_values = []
y_values = []

def extract_last_number(line):
    """提取一行中最后一个空格后的数字"""
    try:
        return float(line.strip().split()[-1])
    except (IndexError, ValueError):
        return None

def process_folder(subfolder_path, output_filename):
    x_values = []
    y_values = []

    for filename in os.listdir(subfolder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(subfolder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 14:
                    y = extract_last_number(lines[5])   # 第6行（索引5）
                    x = extract_last_number(lines[13])  # 第14行（索引13）
                    if x is not None and y is not None and x > 0:
                        x_values.append(x)
                        y_values.append(y)
                    else:
                        print(f"{filename} 中存在无效或非正的X值，已跳过。")
                else:
                    print(f"{filename} 行数不足，已跳过。")

    # 绘图
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, c='red', alpha=0.7)
    plt.xscale('log')  # 设置X轴为对数坐标
    plt.xlabel('F_STAR')
    plt.ylabel('lg(L_X/SFR)')
    plt.title('distribution of parameter')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.tight_layout()

    # 保存图像
    output_path = os.path.join(subfolder_path, output_filename)
    plt.savefig(output_path)
    plt.close()
    print(f"{output_filename} 已保存到: {output_path}")

# 遍历文件夹中的所有txt文件
base_path = 'Parameter'
for n in range(5):
    subfolder = os.path.join(base_path, f'LW{n}')
    if os.path.isdir(subfolder):
        process_folder(subfolder, f'parameterWithLW{n}.png')
    else:
        print(f"文件夹 {subfolder} 不存在，已跳过。")