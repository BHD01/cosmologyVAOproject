import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 单文件最强VAO曲线绘制
# 如果文件在当前目录，直接读取（推荐）
filename = '015-k_LW=0.71;-Mcool0=1.95e+05;-mean_fixed.csv'  # 注意文件名中的空格

df = pd.read_csv(filename)

# 确保列为数值类型（防止读取问题）
df['k_perp'] = pd.to_numeric(df['k_perp'], errors='coerce')
df['nu_obs'] = pd.to_numeric(df['nu_obs'], errors='coerce')
df['VAO'] = pd.to_numeric(df['VAO'], errors='coerce')

# 找到 |VAO| 绝对值最大的行
idx_max = np.argmax(np.abs(df['VAO']))
nu_obs_peak = df['nu_obs'].iloc[idx_max]
vao_max = df['VAO'].iloc[idx_max]

print(f"最强信号频率: ν = {nu_obs_peak} MHz")
print(f"对应最强 VAO 值: {vao_max:.6f} mK²")

# 提取该固定 nu_obs 下的所有 k_perp 数据（允许小浮点误差）
mask = np.isclose(df['nu_obs'], nu_obs_peak, rtol=1e-5, atol=1e-3)  # MHz 级别，宽容一些
sub_df = df[mask].sort_values('k_perp')

if len(sub_df) == 0:
    print("警告：未找到匹配的 nu_obs 数据！")
else:
    print(f"该频率切片包含 {len(sub_df)} 个 k_perp 点")

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(sub_df['k_perp'], sub_df['VAO'], marker='o', linestyle='-', linewidth=2, markersize=4, color='blue')

ax.set_xlabel(r'$k_{\perp} \ (\rm{Mpc}^{-1})$', fontsize=14)
ax.set_ylabel(r'VAO $(\rm{mK}^2)$', fontsize=14)  # 这里直接用 VAO，因为 y=VAO
ax.set_title(f'VAO at Peak Signal Frequency (ν = {nu_obs_peak} MHz)\n'
             f'File: {filename}', fontsize=16)

ax.grid(True, which='both', ls='--', alpha=0.5)

# 可选：线性或对数 x 轴（功率谱常用对数）
# ax.set_xscale('log')  # 如果想用对数坐标，取消注释

plt.tight_layout()
plt.savefig('single_VAO_peak_spectrum.png', dpi=300)
plt.show()

print("单文件最强频率 VAO 曲线已绘制并保存为 single_VAO_peak_spectrum.png")