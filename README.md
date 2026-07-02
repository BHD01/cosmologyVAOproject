# Cosmology VAO Project

研究宇宙黎明时期（Cosmic Dawn）21厘米信号的项目，利用机器学习方法分析模拟程序生成的21厘米功率谱数据。

## 项目结构

| 目录 | 说明 |
|------|------|
| [`ANN/`](./ANN/) | 使用 **ANN** 分析 21cmvFAST 模拟的 21 cm 三维功率谱图像 |
| [`21cmvFAST/`](./21cmvFAST/) | 使用 **CNN** 分析 21cmvFAST 模拟的 21 cm 三维功率谱图像，估计 LW 反馈模型、恒星形成率及 X 射线强度 |
| [`meanpic/`](./meanpic/) | 处理 21cmFAST-VAO 模拟的 21 cm 二维多频率角功率谱图像，生成平均图像 |
| [`AngularPS/`](./AngularPS/) | 使用 **CNN** 分析 21cmFAST-VAO 模拟的 21 cm 二维多频率角功率谱图像中的 **VAO 信号**（可能含热噪声），估计 LW 反馈强度 |
| [`modelD/`](./modelD/) | 使用 **CNN** 分析 21cmFAST-VAO 模拟的 21 cm 二维多频率角功率谱图像中的 **VAO 信号**，估计暗晕冷却阈值质量 |

## 方法

- **21cmvFAST / 21cmFAST-VAO**: 宇宙黎明时期 21 cm 信号模拟程序
- **ANN**: 人工神经网络
- **CNN**: 卷积神经网络
- **VAO**: 可能指特定天文信号特征
- **LW 反馈**: Lyman-Werner 反馈，影响早期星系形成的辐射反馈机制
