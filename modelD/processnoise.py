import os
import pandas as pd

folder = "caseC"

for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(folder, filename)

        df = pd.read_csv(filepath)

        # 核心操作：nu_obs < 60 的 VAO 置 0
        df.loc[df["nu_obs"] < 60, "VAO"] = 0.0

        # 覆盖保存
        df.to_csv(filepath, index=False)

        print(f"Processed: {filepath}")
