import os
import pandas as pd
import numpy as np
import torch
import glob

# 定义文件夹路径
data_dirs = {
    'test': 'dataForTesting/caseB'
}

# 保存张量的输出路径
output_dir = 'processed_tensors/caseB'
os.makedirs(output_dir, exist_ok=True)

def process_csv_files(data_dir, mean, std):
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    if not csv_files:
        print(f"警告：{data_dir} 中未找到CSV文件")
        return None, None
    
    images = []
    labels = []
    
    sample_df = None
    for csv_file in csv_files:
        try:
            sample_df = pd.read_csv(csv_file)
            if sample_df[['k_perp', 'nu_obs', 'VAO']].isna().any().any():
                print(f"警告：{csv_file} 包含NaN值，将跳过无效行")
                sample_df = sample_df.dropna()
            if not sample_df.empty:
                break
        except Exception as e:
            print(f"错误：无法读取 {csv_file}，错误信息：{e}")
            continue
    
    if sample_df is None or sample_df.empty:
        print(f"错误：{data_dir} 中没有有效的CSV文件")
        return None, None
    
    k_perp_values = sorted(sample_df['k_perp'].unique())
    nu_obs_values = sorted(sample_df['nu_obs'].unique())
    height = len(nu_obs_values)
    width = len(k_perp_values)
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        try:
            parts = filename.split(';')
            klw_part = parts[0].split('=')[1]
            mcool_part = parts[1].split('=')[1]
            klw = float(klw_part)
            mcool = float(mcool_part)
            if not (abs(klw - round(klw, 2)) < 1e-10):
                print(f"警告：{csv_file} 的 klw ({klw}) 不是两位小数，跳过")
                continue
            mcool_str = f"{mcool:.2e}"
            if len(mcool_str.split('e')[0].replace('.', '')) > 3:
                print(f"警告：{csv_file} 的 mcool ({mcool}) 有效数字超过三位，跳过")
                continue
            print(f"文件 {csv_file}：klw = {klw}, mcool = {mcool}")
        except (IndexError, ValueError) as e:
            print(f"警告：{csv_file} 文件名格式错误，跳过：{e}")
            continue
        
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            print(f"错误：无法读取 {csv_file}，错误信息：{e}")
            continue
        
        df = df.dropna()
        if df.empty:
            print(f"警告：{csv_file} 在移除NaN后为空，跳过")
            continue
        
        image = np.zeros((height, width), dtype=np.float32)
        valid_file = True
        
        for _, row in df.iterrows():
            try:
                k_idx = np.argmin(np.abs(k_perp_values - row['k_perp']))
                nu_idx = np.argmin(np.abs(nu_obs_values - row['nu_obs']))
                if abs(k_perp_values[k_idx] - row['k_perp']) > 1e-10:
                    raise ValueError(f"k_perp 偏差过大: {row['k_perp']} vs {k_perp_values[k_idx]}")
                if abs(nu_obs_values[nu_idx] - row['nu_obs']) > 1e-10:
                    raise ValueError(f"nu_obs 偏差过大: {row['nu_obs']} vs {nu_obs_values[nu_idx]}")
                image[nu_idx, k_idx] = row['VAO']
            except ValueError as e:
                print(f"警告：{csv_file} 中无效的 k_perp 或 nu_obs 值：{row.to_dict()}，跳过该行")
                valid_file = False
                break
        
        if valid_file:
            images.append(image)
            # 归一化标签
            label = torch.tensor([klw, mcool], dtype=torch.float32)
            label_normalized = (label - mean) / std
            labels.append(label_normalized.numpy())
    
    if not images:
        print(f"错误：{data_dir} 中没有有效的数据文件")
        return None, None
    
    images_tensor = torch.tensor(np.array(images), dtype=torch.float32).unsqueeze(1)  # 形状：(N, 1, H, W)
    labels_tensor = torch.tensor(labels, dtype=torch.float32)  # 形状：(N, 2)
    
    return images_tensor, labels_tensor

# 处理整个数据集以生成统一的归一化器
label_stats = torch.load('processed_tensors/caseB/label_stats.pt')
global_mean, global_std = label_stats['mean'], label_stats['std']

# 处理每个数据集
for dataset_type, data_dir in data_dirs.items():
    print(f"处理 {dataset_type} 数据集...")
    images_tensor, labels_tensor = process_csv_files(data_dir, global_mean, global_std)
    
    if images_tensor is not None and labels_tensor is not None:
        output_file = os.path.join(output_dir, f'{dataset_type}_exdata.pt')
        torch.save({
            'images': images_tensor,
            'labels': labels_tensor  # 保存归一化后的标签
        }, output_file)
        print(f"{dataset_type} 数据已保存到 {output_file}")
        print(f"张量形状: {images_tensor.shape}, 标签数量: {len(labels_tensor)}")
    else:
        print(f"{dataset_type} 数据集处理失败，跳过保存")

print("所有数据集处理完成！")