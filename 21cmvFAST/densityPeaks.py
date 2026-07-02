#用局部密度聚类从一系列参数中挑选适合作为测试集的数据样本

import os
import matplotlib.pyplot as plt
import numpy as np
import csv

def extract_last_number(line):
    try:
        return float(line.strip().split()[-1])
    except (IndexError, ValueError):
        return None

def collect_data(folder_path, label):
    x_vals, y_vals, filenames, sources = [], [], [], []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            path = os.path.join(folder_path, filename)
            with open(path, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 14:
                    y = extract_last_number(lines[5])
                    x = extract_last_number(lines[13])
                    if x is not None and y is not None and x > 0:
                        x_vals.append(x)
                        y_vals.append(y)
                        filenames.append(filename)
                        sources.append(label)
    return np.array(x_vals), np.array(y_vals), filenames, sources

# 主路径
base_path = 'Parameter'

# 收集 LW0 和 LW1~LW4 数据
lw0_x, lw0_y, lw0_names, _ = collect_data(os.path.join(base_path, 'V0L0'), 'V0L0')

other_x, other_y, other_names, other_sources = [], [], [], []
for i in range(1, 5):
    x, y, names, sources = collect_data(os.path.join(base_path, f'V0L{i}'), f'V0L{i}')
    other_x.extend(x)
    other_y.extend(y)
    other_names.extend(names)
    other_sources.extend(sources)

other_x = np.array(other_x)
other_y = np.array(other_y)

# === 🚩 数据归一化（X 取 log，再归一化；Y 线性归一化） ===

# 全部 X（包括 LW0 和其他）一起归一化
all_log_x = np.log10(np.concatenate([lw0_x, other_x]))
x_min, x_max = np.min(all_log_x), np.max(all_log_x)
all_log_x_norm = (all_log_x - x_min) / (x_max - x_min)

# 分开归一化后的 X
lw0_x_norm = all_log_x_norm[:len(lw0_x)]
other_x_norm = all_log_x_norm[len(lw0_x):]

# Y 坐标归一化
all_y = np.concatenate([lw0_y, other_y])
y_min, y_max = np.min(all_y), np.max(all_y)
lw0_y_norm = (lw0_y - y_min) / (y_max - y_min)
other_y_norm = (other_y - y_min) / (y_max - y_min)

# 邻域搜索参数（归一化空间中定义）
radius = 0.05

# === 计算邻域点数 ===
counts = []
neighbors_per_point = []

for xi, yi in zip(lw0_x_norm, lw0_y_norm):
    dists = np.sqrt((other_x_norm - xi)**2 + (other_y_norm - yi)**2)
    mask = dists <= radius
    neighbors = list(zip(
        np.array(other_sources)[mask],
        other_x[mask],
        other_y[mask],
        np.array(other_names)[mask]
    ))
    counts.append(len(neighbors))
    neighbors_per_point.append(neighbors)

# Top 10 高密度点索引
top_indices = np.argsort(counts)[-10:]

highlight_x = lw0_x[top_indices]
highlight_y = lw0_y[top_indices]
highlight_names = [lw0_names[i] for i in top_indices]
highlight_counts = [counts[i] for i in top_indices]
highlight_neighbors = [neighbors_per_point[i] for i in top_indices]

# === 输出到 CSV ===
output_csv = os.path.join(base_path, 'LW0_top10_with_neighbors.csv')
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LW0_File', 'LW0_X', 'LW0_Y', 'Neighbor_LWn', 'Neighbor_X', 'Neighbor_Y', 'Neighbor_File'])
    
    for i in range(10):
        lw0_file = highlight_names[i]
        x0, y0 = highlight_x[i], highlight_y[i]
        neighbors = highlight_neighbors[i]
        if not neighbors:
            writer.writerow([lw0_file, x0, y0, '', '', '', ''])
        for lw_source, x, y, fname in neighbors:
            writer.writerow([lw0_file, x0, y0, lw_source, x, y, fname])

print(f"数据已保存到：{output_csv}")

# === 绘图（使用原始坐标） ===
plt.figure(figsize=(10, 7))

plt.scatter(lw0_x, lw0_y, label='LW0', color='blue', alpha=0.5)
for i in range(1, 5):
    x, y, _, _ = collect_data(os.path.join(base_path, f'LW{i}'), f'LW{i}')
    plt.scatter(x, y, label=f'LW{i}', alpha=0.6)

plt.scatter(highlight_x, highlight_y, color='black', marker='*', s=120, label='LW0 Top10 density peak')

plt.xscale('log')
plt.xlabel('X (log scale)')
plt.ylabel('Y')
plt.title(f'choosing data for testing using density peaks (r={radius} in [0,1] space)')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()
plt.tight_layout()

# 保存图像
output_path = os.path.join(base_path, 'parameter_top10_LW0_normalized.png')
plt.savefig(output_path)
plt.close()

# 输出信息
print(f"图已保存: {output_path}")
print("\nTop 10 LW0 高密度点（文件名 和 邻域点数）：")
for name, c in zip(highlight_names, highlight_counts):
    print(f"  {name:<40}  --> 邻域内非LW0点数: {c}")
