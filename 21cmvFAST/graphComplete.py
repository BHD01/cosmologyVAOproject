#为了挑选合适的测试集编写的临时程序，在参数空间展示所有21cmvFAST程序的天体物理参数采样
#需要将所有参数按照LW强度分别保存在不同的文件夹里，文件夹用LWn命名
#本程序是parameterGraph.py的叠加形式

import os
import matplotlib.pyplot as plt

def extract_last_number(line):
    """提取一行中最后一个空格后的数字"""
    try:
        return float(line.strip().split()[-1])
    except (IndexError, ValueError):
        return None

def collect_data_from_folder(folder_path):
    """从单个子文件夹中收集 X 和 Y 数据"""
    x_vals, y_vals = [], []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 14:
                    y = extract_last_number(lines[5])
                    x = extract_last_number(lines[13])
                    if x is not None and y is not None and x > 0:
                        x_vals.append(x)
                        y_vals.append(y)
    return x_vals, y_vals

# 主执行部分：叠加绘图
base_path = 'Parameter'
colors = ['blue', 'green', 'red', 'orange', 'purple']
markers = ['o', 's', '^', 'D', 'x']  # 不同的标记形状
labels = [f'LW{n}' for n in range(5)]

plt.figure(figsize=(10, 7))

for n in range(5):
    folder = os.path.join(base_path, f'LW{n}')
    if os.path.isdir(folder):
        x, y = collect_data_from_folder(folder)
        plt.scatter(x, y, label=labels[n], color=colors[n], marker=markers[n], alpha=0.7)
    else:
        print(f"跳过不存在的文件夹: {folder}")

plt.xscale('log')
plt.xlabel('F_STAR')
plt.ylabel('lg(L_X/SFR)')
plt.title('distribution of parameter')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend(title='LW Feedback')
plt.tight_layout()

# 保存图像
output_path = os.path.join(base_path, 'parameter_combined.png')
plt.savefig(output_path)
plt.close()
print(f"叠加图已保存到: {output_path}")
