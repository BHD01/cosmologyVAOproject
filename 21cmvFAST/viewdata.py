import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, x_data, y_data):
        # 重排维度：(N, H, W, C) -> (N, C, H, W)
        x_data = np.transpose(x_data, (0, 3, 1, 2))  # 从 (N, 78, 20, 1) 到 (N, 1, 78, 20)
        self.x_data = torch.tensor(x_data, dtype=torch.float32)
        self.y_data = torch.tensor(y_data, dtype=torch.float32)  # Shape: (N, 3)

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        return self.x_data[idx], self.y_data[idx]

def load_data():
    # 加载 NumPy 文件
    X_train = np.load('tensorForTesting/processed/X_train.npy')  # (400, 78, 20, 1)
    y_train = np.load('tensorForTesting/processed/y_train.npy')  # (400, 3)
    X_valid = np.load('tensorForTesting/processed/X_val.npy')  # (50, 78, 20, 1)
    y_valid = np.load('tensorForTesting/processed/y_val.npy')  # (50, 3)
    X_test = np.load('tensorForTesting/processed/X_test.npy')   # (50, 78, 20, 1)
    y_test = np.load('tensorForTesting/processed/y_test.npy')   # (50, 3)

    # 创建数据集
    train_dataset = CustomDataset(X_train, y_train)
    valid_dataset = CustomDataset(X_valid, y_valid)
    test_dataset = CustomDataset(X_test, y_test)

    # 创建 DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=32)
    test_loader = DataLoader(test_dataset, batch_size=32)

    print(f"训练集: {len(train_dataset)} 样本, 数据形状 {train_dataset[0][0].shape}, 标签形状 {y_train.shape}")
    print(f"验证集: {len(valid_dataset)} 样本, 数据形状 {valid_dataset[0][0].shape}, 标签形状 {y_valid.shape}")
    print(f"测试集: {len(test_dataset)} 样本, 数据形状 {test_dataset[0][0].shape}, 标签形状 {y_test.shape}")
    return train_loader, valid_loader, test_loader

if __name__ == "__main__":
    train_loader, valid_loader, test_loader = load_data()