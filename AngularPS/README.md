# AngularPS — CNN 分析 21 cm 二维角功率谱（VAO 信号）

使用 **卷积神经网络（CNN）** 分析模拟程序 **21cmFAST-VAO** 生成的宇宙黎明时期 21 cm **二维多频率角功率谱** 图像中的 **VAO 信号**（可能含热噪声）。

CNN 可以估计出 **LW 反馈强度**。

## 文件说明

### 脚本

| 文件 | 说明 |
|------|------|
| `data.py` | 数据加载与预处理 |
| `data_onepara.py` | 单参数数据处理 |
| `count.py` | 文件计数统计 |
| `move.py` / `movecsv.py` | 文件/CSV 移动工具 |
| `missingfiles.py` | 缺失文件检查 |
| `renameData.py` | 数据重命名 |
| `shuffle_files.py` | 文件打乱 |
| `cnn_*.ipynb` | 各实验配置的 CNN 笔记本 |

### CNN 实验配置

| 笔记本 | 说明 |
|--------|------|
| `cnn.ipynb` | 基础 CNN |
| `cnn_fix.ipynb` | 修复版本 |
| `cnn_meankm.ipynb` | 使用 mean km 数据 |
| `cnn_modelA.ipynb` | Model A 配置 |
| `cnn_modelB.ipynb` | Model B 配置 |
| `cnn_modelD.ipynb` | Model D 配置 |
| `cnn_modelDex.ipynb` | Model Dex 配置 |
| `cnn_noise10000.ipynb` | 含热噪声（10000 样本） |
| `cnn_noise10000_fix.ipynb` | 含热噪声修复版 |
| `cnn_smallpic.ipynb` | 小图像测试 |

### 数据子目录

- `dataForLearning/` — 训练数据
- `dataForTesting/` — 测试数据
- `dataForValidation/` — 验证数据
- `processed_tensors/` — 预处理后的张量数据（`.pt`）及标签统计
- `dataForLearning/modelB/`、`dataForLearning/modelD/` 等 — 各模型配置的训练数据

### 其他

| 文件 | 说明 |
|------|------|
| `cnntraining.txt` | 训练日志 |
| `sbatchPython.sh` | 集群提交脚本 |
| `job_output_*.log` / `job_error_*.log` | 作业输出/错误日志 |

## 背景

- **21cmFAST-VAO**: 模拟宇宙黎明时期 21 cm 信号的程序
- **二维多频率角功率谱**: 21 cm 信号在不同频率和角度上的涨落统计
- **VAO 信号**: 项目关注的特定天文信号特征
- **LW 反馈**: Lyman-Werner 辐射反馈
