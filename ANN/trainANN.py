import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import os

"""
本程序通过模拟功率谱生成ANN神经网络，目前整个项目已经不需要该程序，当前仅以归档目的保留。
"""

# 1. 数据加载和预处理
def load_data_from_folders(lw0_folder, lw3_folder):
    """
    从两个文件夹加载张量数据，并为它们分配对应的 LW 值。
    
    参数:
    lw0_folder (str): 存放 LW=0 张量的文件夹路径。
    lw3_folder (str): 存放 LW=3 张量的文件夹路径。
    
    返回:
    torch.Tensor, torch.Tensor: 张量数据和 LW 值的 PyTorch 张量。
    """
    tensors = []
    lw_values = []
    
    # 加载 LW=0 数据
    for file_name in os.listdir(lw0_folder):
        file_path = os.path.join(lw0_folder, file_name)
        if file_path.endswith('.npy'):
            tensors.append(np.load(file_path))
            lw_values.append(0)
    
    # 加载 LW=3 数据
    for file_name in os.listdir(lw3_folder):
        file_path = os.path.join(lw3_folder, file_name)
        if file_path.endswith('.npy'):
            tensors.append(np.load(file_path))
            lw_values.append(3)
    
    # 转换为 PyTorch 张量
    X = torch.tensor(np.array(tensors), dtype=torch.float32)
    y = torch.tensor(np.array(lw_values), dtype=torch.float32)
    
    return X, y

# 2. 定义神经网络
class SimpleANN(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super(SimpleANN, self).__init__()
        self.model = nn.Sequential(
            nn.Flatten(),  # 展平三维张量
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, x):
        return self.model(x)

# 3. 训练函数
def train_model(model, train_loader, val_loader, epochs=50, lr=0.001):
    """
    训练模型。
    
    参数:
    model (nn.Module): 神经网络模型。
    train_loader (DataLoader): 训练数据加载器。
    val_loader (DataLoader): 验证数据加载器。
    epochs (int): 训练轮数。
    lr (float): 学习率。
    """
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            y_pred = model(X_batch).squeeze()
            loss = criterion(y_pred, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        
        # 验证
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                y_pred = model(X_batch).squeeze()
                loss = criterion(y_pred, y_batch)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        
        print(f"Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

# 4. 主程序
if __name__ == "__main__":
    # 假设你的 LW0 和 LW3 文件夹路径如下
    lw0_folder = "LW0"
    lw3_folder = "LW3"
    
    # 加载数据
    X, y = load_data_from_folders(lw0_folder, lw3_folder)

    # 选择设备 (GPU 或 CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 将模型移到 GPU（如果可用）
    input_dim = X[0].numel()  # 展平后的输入大小
    model = SimpleANN(input_dim=input_dim)
    model.to(device)  # 将模型移动到 GPU/CPU
        
    # 将数据也移到 GPU（如果可用）
    X, y = X.to(device), y.to(device)
    
    # 数据集划分
    dataset = TensorDataset(X, y)
    train_size = int(0.9 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=50, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4)
    
    # 定义模型
    input_dim = X[0].numel()  # 展平后的输入大小
    model = SimpleANN(input_dim=input_dim)
    
    # 训练模型
    train_model(model, train_loader, val_loader)

    # 保存模型
    torch.save(model.state_dict(), "lw_predictor.pth")
    print("Model saved as lw_predictor.pth")
