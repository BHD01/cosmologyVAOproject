import os
import numpy as np
import glob
import re
from collections import defaultdict
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib

"""
本程序将21cmvFAST生成的功率谱文件转换为数据张量。
- 数据集已预先划分为训练集、验证集、测试集。
- 每个目录直接包含所有样本的a_b_c_z.txt文件，按[a, b, c]分组为样本（每组78个文件）。
- 每个文件过滤k在[0.03, 0.2]。
- 从文件名a_b_c_z.txt提取标签：[a (LWfeedback, 0~4), b (F_STAR, 10^-2.5~10^-1.5), c (LX, 35~40)]。
- 输出数据张量形状 (num_samples, 78, 20, 1)，标签张量 (num_samples, 3)。
- 包含归一化并保存数据和归一化器。
"""

def parse_filename(filename):
    """
    从文件名a_b_c_z.txt提取标签 [a, b, c]和z值。
    
    参数:
    filename (str): 文件名，如 '3_3.162e-02_37.5_12.34.txt'
    
    返回:
    tuple: (a, b, c) 标签值
    """
    match = re.match(r'(\d)_([\d.eE-]+)_([\d.]+)_([\d.]+)\.txt', os.path.basename(filename))
    if not match:
        raise ValueError(f"Invalid filename: {filename}")
    a = float(match.group(1))  # LW反馈 (0~4)
    b = float(match.group(2))  # F_STAR (e.g., 3.162e-2)
    c = float(match.group(3))  # LX (e.g., 37.5)
    z = float(match.group(4))  # 红移 (e.g., 12.34)
    return a, b, c, z

def load_sample(files):
    """
    加载单个样本的78个txt文件，处理功率谱并提取标签。
    过滤k在[0.03, 0.2]后需正好20个点，否则报告错误。
    20这个数由21cmvFAST的box大小决定。
    
    参数:
    files (list): 样本目录，包含78个a_b_c_z.txt文件
    
    返回:
    tuple: 数据张量 (78, 20, 1), 标签 [a, b, c]
    """
    data_slices = []
    z_values = []
    labels = None

    # 遍历所有符合文件模式的txt文件
    for file_name in sorted(files, key=lambda x: float(os.path.basename(x).split('_')[-1].replace('.txt', ''))):
        # 提取标签和z值
        a, b, c, z = parse_filename(file_name)
        z_values.append(z)
        
        # 加载数据，三列格式为 k, E, err，仅保留前两行
        data = np.loadtxt(file_name)
        k = data[:, 0]    # 第一列是波数k
        E = data[:, 1]    # 第二列是功率E
        
        # 只保留k在[0.03, 0.2]范围内的数据
        mask = (k >= 0.03) & (k <= 0.2)
        k_filtered = k[mask]
        E_filtered = E[mask]
        
        # 验证是否有20个点
        if len(k_filtered) != 20:
            raise ValueError(f"文件 {file_name} 过滤k=[0.03, 0.2]后点数不为20: {len(k_filtered)}")
        
        # 将 k、z 和 E 合并成一个三维结构
        data_slices.append(E_filtered)

        # 提取标签（只需从一个文件）
        if labels is None:
            labels = parse_filename(file_name)

    # 验证是否覆盖78个红移
    if len(data_slices) != 78:
        raise ValueError(f"样本 {files} 文件数不为78: {len(data_slices)}")
    
    # 按照 z 排序
    sorted_indices = np.argsort(z_values)
    data_slices = [data_slices[i] for i in sorted_indices]

    # 转换为张量(78, 20, 1)
    data_tensor = np.array(data_slices)[:, :, np.newaxis]
    return data_tensor, labels

def load_and_process_dataset(data_dir):
    """
    加载指定目录的数据集，返回数据张量和标签。
    
    参数:
    data_dir (str): 数据目录，包含a_b_c_z.txt文件
    
    返回:
    tuple: 数据张量 (num_samples, 78, 20, 1), 标签 (num_samples, 3)
    """
    # 按 [a, b, c] 分组文件
    sample_groups = defaultdict(list)
    for file_name in glob.glob(os.path.join(data_dir, "*.txt")):
        a, b, c, _ = parse_filename(file_name)
        sample_groups[(a, b, c)].append(file_name)

    X = []
    y = []
    
    for (a, b, c), files in sorted(sample_groups.items()):
        try:
            data_tensor, labels = load_sample(files)
            X.append(data_tensor)
            y.append(labels)
        except Exception as e:
            print(f"跳过样本 {[a, b, c]}: {e}")
            continue
    
    if not X:
        raise ValueError(f"未找到有效样本在 {data_dir}")
    
    X = np.array(X)  # (num_samples, 78, 20, 1)
    y = np.array(y)  # (num_samples, 3)
    
    return X, y

def normalize_data(X_train, y_train, X_val, y_val, X_test, y_test, output_dir):
    """
    归一化数据和标签，基于训练集拟合归一化器，保存归一化器。
    
    参数:
    X_train, y_train: 训练集数据和标签
    X_val, y_val: 验证集数据和标签
    X_test, y_test: 测试集数据和标签
    output_dir (str): 保存归一化器的目录
    
    返回:
    tuple: 归一化后的 X_train, y_train, X_val, y_val, X_test, y_test, 归一化器
    """
    # 功率谱归一化（基于训练集）
    scaler_X = StandardScaler()
    X_train_normalized = scaler_X.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
    X_val_normalized = scaler_X.transform(X_val.reshape(-1, X_val.shape[-1])).reshape(X_val.shape)
    X_test_normalized = scaler_X.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)
    
    # 标签归一化（基于训练集）
    scaler_a = MinMaxScaler()  # a: 0~4 -> [0, 1]
    scaler_b = StandardScaler()  # b: 10^-2.5~10^-1.5
    scaler_c = MinMaxScaler()  # c: 35~40 -> [0, 1]
    
    y_train_a = scaler_a.fit_transform(y_train[:, 0:1])
    y_train_b = scaler_b.fit_transform(y_train[:, 1:2])
    y_train_c = scaler_c.fit_transform(y_train[:, 2:3])
    y_train_normalized = np.hstack([y_train_a, y_train_b, y_train_c])
    
    y_val_a = scaler_a.transform(y_val[:, 0:1])
    y_val_b = scaler_b.transform(y_val[:, 1:2])
    y_val_c = scaler_c.transform(y_val[:, 2:3])
    y_val_normalized = np.hstack([y_val_a, y_val_b, y_val_c])

    y_test_a = scaler_a.transform(y_test[:, 0:1])
    y_test_b = scaler_b.transform(y_test[:, 1:2])
    y_test_c = scaler_c.transform(y_test[:, 2:3])
    y_test_normalized = np.hstack([y_test_a, y_test_b, y_test_c])
    
    # 保存归一化器为pkl文件
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(scaler_X, os.path.join(output_dir, 'scaler_X.pkl'))
    joblib.dump(scaler_a, os.path.join(output_dir, 'scaler_a.pkl'))
    joblib.dump(scaler_b, os.path.join(output_dir, 'scaler_b.pkl'))
    joblib.dump(scaler_c, os.path.join(output_dir, 'scaler_c.pkl'))
    
    return (X_train_normalized, y_train_normalized, X_val_normalized, y_val_normalized, 
            X_test_normalized, y_test_normalized, (scaler_X, scaler_a, scaler_b, scaler_c))

def save_dataset(X, y, output_dir, dataset_name):
    """
    保存数据张量到文件，供查看和进一步操作。
    
    X (ndarray): 数据张量
    y (ndarray): 标签
    output_dir (str): 保存目录
    dataset_name (str): 数据集名称（train/val/test）
    返回: None
    """
    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, f'X_{dataset_name}.npy'), X)
    np.save(os.path.join(output_dir, f'y_{dataset_name}.npy'), y)
    print(f"{dataset_name} 数据集已保存至 {output_dir}: {X.shape[0]} 样本")

def main():
    """
    主函数，处理数据集并保存。
    """
    # 数据目录
    train_dir = "dataForLearning/202505L"
    val_dir = "dataForValidation/202505V"
    test_dir = "dataForTesting/202505T"
    output_dir = "tensorForTesting/202505P"
    
    # 加载数据集
    print("加载训练集...")
    X_train, y_train = load_and_process_dataset(train_dir)
    print(f"训练集加载完成: {X_train.shape[0]} 样本，数据形状 {X_train.shape}, 标签形状 {y_train.shape}")
    
    print("加载验证集...")
    X_val, y_val = load_and_process_dataset(val_dir)
    print(f"验证集加载完成: {X_val.shape[0]} 样本，数据形状 {X_val.shape}, 标签形状 {y_val.shape}")
    
    print("加载测试集...")
    X_test, y_test = load_and_process_dataset(test_dir)
    print(f"测试集加载完成: {X_test.shape[0]} 样本，数据形状 {X_test.shape}, 标签形状 {y_test.shape}")
    
    # 归一化
    print("归一化数据...")
    (X_train_normalized, y_train_normalized, X_val_normalized, y_val_normalized, 
     X_test_normalized, y_test_normalized, scalers) = normalize_data(
        X_train, y_train, X_val, y_val, X_test, y_test, output_dir
    )

    # 保存数据集
    print("保存数据集...")
    save_dataset(X_train_normalized, y_train_normalized, output_dir, "train")
    save_dataset(X_val_normalized, y_val_normalized, output_dir, "val")
    save_dataset(X_test_normalized, y_test_normalized, output_dir, "test")
    
    print("处理完成！")

if __name__ == "__main__":
    main()