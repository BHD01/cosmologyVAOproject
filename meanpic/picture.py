import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# ======================
# 路径
# ======================
directory = '.'

# ======================
# 常量
# ======================
pi = np.pi

# ======================
# 读取 J_LW 映射表
# ======================
J_LW_table = pd.read_csv('J_LW_from_nu_peak.csv')

J_LW_dict = {
    int(row['file_id']): row['J_LW']
    for _, row in J_LW_table.iterrows()
}


# ======================
# 文件名正则
# ======================
pattern = re.compile(
    r'^(-?\d+)-\s*k_LW=(-?\d+\.\d{2});-Mcool0=(-?\d+(?:\.\d+)?e[+-]?\d+);-mean\.csv$'
)

# ======================
# 存储曲线
# ======================
curves = []

for filename in os.listdir(directory):
    if not filename.endswith('mean.csv'):
        continue

    match = pattern.match(filename)
    if not match:
        continue

    file_id = int(match.group(1))   # 002 / 003 / ...
    k = float(match.group(2))
    m = float(match.group(3))

    # ------------------
    # 直接读取 J_LW
    # ------------------
    if file_id not in J_LW_dict:
        print(f"警告：J_LW 表中找不到 {file_id}，跳过")
        continue

    J_LW = J_LW_dict[file_id]

    # ------------------
    # 新定义的 four_pi_pow
    # ------------------
    four_pi_pow = (4 * pi * J_LW * 1e21) ** 0.47
    color_val = m * (1 + k * four_pi_pow)

    filepath = os.path.join(directory, filename)

    try:
        df = pd.read_csv(filepath)
        if list(df.columns) != ['k_perp', 'nu_obs', 'VAO']:
            print(f"警告：{filename} 列名不匹配，跳过")
            continue

        # 找 VAO 峰值频率
        idx_max = np.argmax(np.abs(df['VAO']))
        nu_obs_peak = df['nu_obs'].iloc[idx_max]

        # 提取对应切片
        mask = np.isclose(df['nu_obs'], nu_obs_peak, rtol=1e-5, atol=1e-8)
        sub_df = df[mask].sort_values('k_perp')

        if len(sub_df) == 0:
            print(f"警告：{filename} 未找到匹配行")
            continue

        curves.append({
            'k_perp': sub_df['k_perp'].values,
            'y_raw': sub_df['VAO'].values,
            'nu_obs_peak': nu_obs_peak,
            'color_val': color_val,
            'filename': filename
        })

        print(
            f"{filename}: ν_peak={nu_obs_peak:.3f} MHz, "
            f"J_LW={J_LW:.3e}"
        )

    except Exception as e:
        print(f"读取 {filename} 失败: {e}")

if not curves:
    print("未找到任何符合条件的 mean.csv 文件！")
    exit()

# ======================
# 排序
# ======================
curves.sort(key=lambda x: x['nu_obs_peak'])

# ======================
# 绘图
# ======================
fig, ax = plt.subplots(figsize=(12, 9))

color_vals = [c['color_val'] for c in curves]
vmin, vmax = min(color_vals), max(color_vals)
cmap = plt.cm.rainbow

for curve in curves:
    norm_color = (curve['color_val'] - vmin) / (vmax - vmin) if vmax > vmin else 0.5
    ax.plot(curve['k_perp'], curve['y_raw'],
            color=cmap(norm_color),
            linewidth=2)

ax.set_xlabel(r'$k_{\perp} \ (\rm{Mpc}^{-1})$', fontsize=14)
ax.set_ylabel(r'$k^2 / (2\pi) \Delta P_{\rm{VAO}} (k_{\rm{\perp}}) \ (\rm{mK}^2)$', fontsize=14)

norm = plt.Normalize(vmin=vmin, vmax=vmax)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.04)
cbar.set_label(r'$M_{\rm{cool1}} \ (M_{\odot})$', fontsize=14)

ax.grid(True, which='major', alpha=0.3)
ax.grid(True, which='minor', alpha=0.2)

plt.title('The Wiggle of MAPS at Peak Signal Frequency', fontsize=16)
plt.tight_layout()

output_fig = 'VAO_biggest_spectra_combined.png'
plt.savefig(output_fig, dpi=300, bbox_inches='tight')
plt.show()

print(f"图已保存为 {output_fig}")
