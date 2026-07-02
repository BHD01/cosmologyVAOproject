# ANN — 人工神经网络分析 21 cm 功率谱

早期使用 **人工神经网络（ANN）** 分析模拟程序 **21cmvFAST** 生成的宇宙黎明时期 21 cm **三维功率谱** 图像的案例。

## 文件说明

| 文件 | 说明 |
|------|------|
| `trainANN.py` | ANN 训练脚本 |
| `runPredictor.py` | 运行训练好的模型进行预测 |
| `readTensor.py` | 读取张量数据 |
| `lw_predictor241212.pth` | 训练好的 ANN 模型权重 |
| `debug_predictor.pth` | 调试用模型权重 |

## 背景

- **21cmvFAST**: 模拟宇宙黎明时期 21 cm 信号的半数值模拟程序
- **三维功率谱**: 描述 21 cm 信号在三维空间中的涨落特征
