import os
import re
import numpy as np
import pandas as pd

# ======================
# 常量
# ======================
NU_21 = 1420.40575  # MHz

# ======================
# 路径
# ======================
csv_dir = '.'          # mean.csv 所在目录
txt_dir = './global'   # txt 文件所在目录
output_csv = 'J_LW_from_nu_peak.csv'

# ======================
# 文件名正则
# ======================
pattern = re.compile(
    r'^(\d+)-\s*k_LW=(-?\d+\.\d{2});-Mcool0=(-?\d+(?:\.\d+)?e[+-]?\d+);-mean\.csv$'
)

# ======================
# 结果容器
# ======================
rows = []

# ======================
# 主循环
# ======================
for filename in os.listdir(csv_dir):
    if not filename.endswith('mean.csv'):
        continue

    match = pattern.match(filename)
    if not match:
        continue

    file_id = match.group(1)  # '002' ~ '026'

    # ---- 读 csv ----
    df = pd.read_csv(os.path.join(csv_dir, filename))
    if list(df.columns) != ['k_perp', 'nu_obs', 'VAO']:
        print(f"列名不匹配，跳过 {filename}")
        continue

    # ---- 找 VAO 峰值对应频率 ----
    idx_max = np.argmax(np.abs(df['VAO']))
    nu_obs_peak = df.loc[idx_max, 'nu_obs']

    # ---- ν → z ----
    z_peak = NU_21 / nu_obs_peak - 1

    # ---- 读对应 txt ----
    txt_path = os.path.join(txt_dir, f'{file_id}.txt')
    if not os.path.exists(txt_path):
        print(f"找不到 {txt_path}")
        continue

    data = np.loadtxt(txt_path)
    z_txt = data[:, 0]
    J_LW = data[:, -1]

    # ---- 找最近红移 ----
    idx_closest = np.argmin(np.abs(z_txt - z_peak))
    J_LW_match = J_LW[idx_closest]

    # ---- 保存结果 ----
    rows.append({
        'file_id': file_id,
        'J_LW': J_LW_match
    })

# ======================
# 写出 CSV
# ======================
result_df = pd.DataFrame(rows)
result_df.to_csv(output_csv, index=False)

print(f"已生成文件: {output_csv}")
