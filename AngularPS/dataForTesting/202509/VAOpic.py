import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO  # 如果数据在字符串中；实际使用时可替换为文件读取

# --------------------- 读取数据 ---------------------
# 如果你有完整的 CSV 文件，请直接使用：
df = pd.read_csv('505-k_LW=5.96;-Mcool0=2.55e+05;-18.csv')

# --------------------- 数据整理 ---------------------
# 将数据转成二维矩阵
pivot = df.pivot(index='k_perp', columns='nu_obs', values='VAO')

# 排序，确保坐标轴从低到高排列（热图更易读）
pivot = pivot.sort_index()                  # 按 k_perp 升序
pivot = pivot.sort_index(axis=1)            # 按 nu_obs 升序

# 转为 numpy array 供 matplotlib 使用
data = pivot.values

# 获取坐标轴标签
k_perp_values = pivot.index.tolist()       # y轴：k_perp
nu_obs_values = pivot.columns.tolist()     # x轴：nu_obs

# --------------------- 绘制热图 ---------------------
plt.figure(figsize=(12, 8))

# 使用 matplotlib 的 imshow 绘制热图
im = plt.imshow(
    data,
    cmap='coolwarm',       # 红蓝配色，适合正负值
    aspect='auto',         # 自动调整宽高比
    origin='lower',        # 原点在左下角（与矩阵习惯一致）
    extent=[nu_obs_values[0], nu_obs_values[-1], k_perp_values[0], k_perp_values[-1]],
    vmin=-np.nanmax(np.abs(data)),  # 对称颜色范围（可选）
    vmax=np.nanmax(np.abs(data))
)

# 设置坐标轴
plt.xlabel('nu_obs (frequency)')
plt.ylabel('k_perp')

# 设置刻度与标签
plt.xticks(nu_obs_values, rotation=45)
plt.yticks(k_perp_values)

# 添加网格线（对应每个格子）
plt.grid(True, which='major', color='white', linewidth=1)
plt.gca().set_xticks([x - (nu_obs_values[1] - nu_obs_values[0])/2 for x in nu_obs_values], minor=True)
plt.gca().set_yticks([y - (k_perp_values[1] - k_perp_values[0])/2 for y in k_perp_values], minor=True)
plt.gca().grid(True, which='minor', color='gray', linewidth=0.5)

# 在每个格子上显示数值（如果数据量不大）
for i in range(len(k_perp_values)):
    for j in range(len(nu_obs_values)):
        value = data[i, j]
        if not np.isnan(value):
            plt.text(nu_obs_values[j], k_perp_values[i], f'{value:.3f}',
                     ha='center', va='center', color='black', fontsize=8)

# 颜色条
cbar = plt.colorbar(im)
cbar.set_label('VAO')

plt.title('Heatmap of VAO(k_perp, nu_obs) - Pure Matplotlib')
plt.tight_layout()
output_fig = 'VAO.png'
plt.savefig(output_fig, dpi=300, bbox_inches='tight')
plt.show()