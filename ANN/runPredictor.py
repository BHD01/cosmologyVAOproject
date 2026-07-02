import torch
import numpy as np
import os

"""
本程序使用训练好的ANN模型预测测试集张量。
目前处于归档状态，未来在CNN模型预测中作为参考将酌情解除归档状态。
"""

class SimpleANN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=512):
        super(SimpleANN, self).__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(input_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, x):
        return self.model(x)

def load_model(pth_file, input_dim):
    model = SimpleANN(input_dim=input_dim)
    model.load_state_dict(torch.load(pth_file))  # 加载权重
    model.eval()  # 切换到评估模式
    return model

def predict_from_npy(model, npy_folder, output_file):
    """
    使用训练好的模型对文件夹中的 .npy 张量进行预测。

    参数:
    - model: 训练好的模型
    - npy_folder (str): 存放 .npy 文件的文件夹路径
    - output_file (str): 保存预测结果的文件路径

    输出:
    - 每个文件的预测值将被保存到 `output_file` 中
    """
    results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 检查设备
    model.to(device)

    # 遍历 .npy 文件夹
    for file in os.listdir(npy_folder):
        if file.endswith(".npy"):
            file_path = os.path.join(npy_folder, file)
            tensor = np.load(file_path)  # 加载 .npy 文件
            tensor = torch.tensor(tensor, dtype=torch.float32).unsqueeze(0).to(device)  # 添加批次维度

            # 预测
            with torch.no_grad():
                prediction = model(tensor).item()
            
            # 保存结果
            results.append((file, prediction))
            print(f"File: {file}, Predicted LW: {prediction:.4f}")

    # 保存结果到文件
    with open(output_file, "w") as f:
        for file, prediction in results:
            f.write(f"{file},{prediction:.4f}\n")

    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    # 假设输入张量的形状为 (78, 20, 3)
    input_shape = (78, 20, 3)
    input_dim = np.prod(input_shape)  # 展平后的输入大小

    # 加载模型
    model = load_model("lw_predictor_z.pth", input_dim)

    # 文件夹路径和输出文件
    npy_folder = "./tensorForTesting/LW3/"  # 存放 .npy 文件的文件夹路径
    output_file = "prediction3z.csv"  # 保存预测结果的文件路径

    # 执行预测
    predict_from_npy(model, npy_folder, output_file)

