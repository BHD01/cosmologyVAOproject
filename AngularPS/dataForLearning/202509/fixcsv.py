import pandas as pd
import numpy as np
from pathlib import Path

root_dir = Path("./")
suffix = "_fixed"


def fix_single_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)

        required_cols = {"k_perp", "nu_obs", "VAO"}
        if not required_cols.issubset(df.columns):
            print(f"[跳过] 缺列: {csv_path}")
            return

        # 唯一坐标并排序
        kt = np.sort(df["k_perp"].unique())
        nu = np.sort(df["nu_obs"].unique())

        n_k = len(kt)
        n_nu = len(nu)

        if n_k * n_nu != len(df):
            print(f"[跳过] 尺寸不匹配: {csv_path}")
            return

        # ==================================================
        # 关键区别在这里！
        # 原错误保存时：VAO 是按 (nu, k) flatten 的
        # ==================================================
        vao_as_nu_k = df["VAO"].values.reshape(n_nu, n_k)

        # 现在 vao_as_nu_k[i_nu, j_k] 是正确的物理值

        # ==================================================
        # 按 CSV 要求的 (k, nu) 顺序重新写出
        # ==================================================
        k_grid, nu_grid = np.meshgrid(kt, nu, indexing="ij")

        df_fixed = pd.DataFrame({
            "k_perp": k_grid.ravel(),
            "nu_obs": nu_grid.ravel(),
            "VAO": vao_as_nu_k.T.ravel()
        })

        #out_path = csv_path.with_name(csv_path.stem + suffix + csv_path.suffix)
        df_fixed.to_csv(csv_path, index=False)

        print(f"[修复] {csv_path}")

    except Exception as e:
        print(f"[错误] {csv_path}: {e}")


for csv_file in root_dir.rglob("*.csv"):
    if csv_file.stem.endswith(suffix):
        continue
    fix_single_csv(csv_file)

print("全部完成 ✔")
