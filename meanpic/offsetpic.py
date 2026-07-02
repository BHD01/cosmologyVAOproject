import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# ======================
# 设置路径和常量
# ======================
directory = '.'
pi = np.pi

# ======================
# 读取 J_LW 映射表
# ======================
J_LW_table = pd.read_csv('J_LW_from_nu_peak.csv')
J_LW_dict = {int(r['file_id']): r['J_LW'] for _, r in J_LW_table.iterrows()}

# ======================
# 文件名正则
# ======================
pattern = re.compile(
    r'^(-?\d+)-\s*k_LW=(-?\d+\.\d{2});-Mcool0=(-?\d+(?:\.\d+)?e[+-]?\d+);-mean\.csv$'
)

# ======================
# 读取所有曲线
# ======================
curves = []

for fn in os.listdir(directory):
    if not fn.endswith('mean.csv'):
        continue
    m = pattern.match(fn)
    if not m:
        continue

    file_id = int(m.group(1))
    k_LW = float(m.group(2))
    Mcool0 = float(m.group(3))

    if file_id not in J_LW_dict:
        print(f"警告：{file_id} 不在 J_LW 表中")
        continue

    df = pd.read_csv(fn)
    if list(df.columns) != ['k_perp', 'nu_obs', 'VAO']:
        print(f"警告：{fn} 列名不匹配")
        continue

    idx = np.argmax(np.abs(df['VAO']))
    nu_peak = df['nu_obs'].iloc[idx]

    mask = np.isclose(df['nu_obs'], nu_peak, rtol=1e-5, atol=1e-8)
    sub = df[mask].sort_values('k_perp')
    if len(sub) == 0:
        continue

    J_LW = J_LW_dict[file_id]
    four_pi_pow = (4 * pi * J_LW * 1e21) ** 0.47
    Mcool1 = Mcool0 * (1 + k_LW * four_pi_pow)

    curves.append({
        'k_perp': sub['k_perp'].values,
        'y': sub['VAO'].values,
        'nu': nu_peak,
        'Mcool1': Mcool1,
        'color_val': Mcool1
    })

if not curves:
    raise RuntimeError("未读取到任何曲线")

# ======================
# 频率分组 + 组内排序
# ======================
def nu_key(nu, tol=1e-3):
    return round(nu / tol) * tol

freq_groups = defaultdict(list)
for c in curves:
    freq_groups[nu_key(c['nu'])].append(c)

# ======================
# 构造绘图顺序
# ======================
ordered_curves = []

for fk in sorted(freq_groups.keys()):  # 低频在前（靠上）
    group = freq_groups[fk]
    # 组内按 Mcool1 从小到大排列（越小越靠上）
    group_sorted = sorted(group, key=lambda c: c['Mcool1'])

    print(f"\nFrequency group {fk:.3f} MHz:")
    for c in group_sorted:
        print(f"  Mcool1 = {c['Mcool1']:.6e}")

    ordered_curves.extend(group_sorted)

# ======================
# offset 计算
# ======================
all_y = np.concatenate([c['y'] for c in ordered_curves])
y_range = np.max(all_y) - np.min(all_y)

offset_step = 0.25 * y_range  # 同频率曲线间距
freq_gap_boost = 3.0          # 不同频率组额外间隔

indices = []
current_index = 0
last_fk = None

for c in ordered_curves:
    fk = nu_key(c['nu'])
    if last_fk is not None and fk != last_fk:
        current_index += freq_gap_boost
    indices.append(current_index)
    current_index += 1
    last_fk = fk

# ======================
# 绘图
# ======================
fig, ax = plt.subplots(figsize=(12, 9))
cmap = plt.cm.rainbow
vals = [c['color_val'] for c in ordered_curves]
vmin, vmax = min(vals), max(vals)

all_y_offset = []
for c, idx in zip(ordered_curves, indices):
    y_plot = c['y'] - idx * offset_step
    all_y_offset.append(y_plot)

all_y_offset = np.concatenate(all_y_offset)
global_min = all_y_offset.min()
global_max = all_y_offset.max()
y_range = global_max - global_min

# 为了让 y=0 尽量在图中间，设置对称的 ylim（留一点 margin）
margin = 0.05 * y_range
ax.set_ylim(global_min - margin, global_max + margin)

# 绘制所有曲线
current_fk = None
for i, (c, idx) in enumerate(zip(ordered_curves, indices)):
    fk = nu_key(c['nu'])
    y_plot = c['y'] - idx * offset_step
    norm = (c['color_val'] - vmin) / (vmax - vmin) if vmax > vmin else 0.5
    ax.plot(c['k_perp'], y_plot, color=cmap(norm), lw=2)

    # === 频率标注：只在每组的第一条（最上面）曲线标注一次 ===
    if fk != current_fk:  # 新频率组开始
        # 在该组最上面那条曲线的右端上方标注
        text_y = y_plot[-1] + 1.0 * offset_step  # 向上偏移一点
        group_curves = [ordered_curves[j] for j in range(i, len(ordered_curves)) 
                        if nu_key(ordered_curves[j]['nu']) == fk]
        all_k = np.concatenate([gc['k_perp'] for gc in group_curves])
        x_mid = np.median(all_k)         # 用中位数，更稳健

        # 水平位置：放在中间，或稍微左移/右移以优化视觉效果
        x_pos = x_mid                    # 正中间
        ax.text(
            x_pos,
            text_y,
            f"{c['nu']:.2f} MHz",
            fontsize=10,
            va='bottom',      # 文字底部对齐标注点
            ha='center',
            weight='bold'     # 可选：加粗更好辨认
        )
        current_fk = fk

ax.set_xlabel(r"$k_\perp\ (\rm Mpc^{-1})$", fontsize=14)
# 修改 y 轴标签，体现真实物理量
ax.set_ylabel(r"$\Delta^2_{21,\rm wiggles} + {\rm offset}\ [\rm mK^2]$", fontsize=14)

# 显示 y 轴刻度，并让 0 尽量在中间
ax.tick_params(axis='y', which='major', labelsize=10)
ax.grid(alpha=0.3, which='both')

# 可选：添加水平线突出 y=0
ax.axhline(0, color='black', linewidth=0.8, alpha=0.7)

# 颜色条保持不变
norm = plt.Normalize(vmin=vmin, vmax=vmax)
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.04)
cbar.set_label(r"$M_{\rm cool1}\ (\rm M_\odot)$", fontsize=14)

plt.tight_layout()
plt.savefig('VAO_biggest_spectra_FINAL.pdf', dpi=300)