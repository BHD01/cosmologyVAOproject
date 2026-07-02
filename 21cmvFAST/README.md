# 21cmvFAST — CNN 分析 21 cm 三维功率谱

使用 **卷积神经网络（CNN）** 分析模拟程序 **21cmvFAST** 生成的宇宙黎明时期 21 cm **三维功率谱** 图像。

CNN 可以估计出以下物理参数：

- **LW 反馈模型** — Lyman-Werner 辐射反馈强度
- **恒星形成率** — 早期星系的恒星形成效率
- **X 射线强度** — 早期宇宙的 X 射线辐射强度

## 文件说明

### 脚本

| 文件 | 说明 |
|------|------|
| `data.py` | 数据加载与预处理 |
| `cnn.ipynb` | CNN 模型主笔记本 |
| `bnn.ipynb` | BNN（贝叶斯神经网络）笔记本 |
| `densityPeaks.py` | 密度峰值分析 |
| `graphComplete.py` | 图表生成 |
| `parameterGraph.py` | 参数关系图 |
| `makeValidation.py` | 验证集制作 |
| `renamedata.py` | 数据重命名工具 |
| `viewdata.py` | 数据可视化 |

### 模型权重

| 文件 | 说明 |
|------|------|
| `best_model.pt` | 最佳 CNN 模型 |
| `best_bnn_model.pt` | 最佳 BNN 模型 |
| `model1.pt` / `model2.pt` | 其他训练模型 |
| `model_novao.pt` | 无 VAO 信号模型 |
| `lw_predictor_z.pth` | LW 反馈预测器 |

### 数据

- `tensorForLearning/` — 训练用张量数据（`.npy`）
- `tensorForTesting/` — 测试用张量数据（`.npy`）及归一化参数（`.pkl`）
- `predictions_table_bnn.csv` — BNN 预测结果表
- `prediction3z.csv` — 红移预测数据

## 背景

- **21cmvFAST**: 基于 21cmFAST 的模拟程序，生成宇宙黎明时期 21 cm 信号
- **三维功率谱**: 21 cm 信号在三维空间中的涨落统计特征
