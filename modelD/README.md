# modelD — CNN 分析 21 cm 二维角功率谱（暗晕冷却阈值质量）

使用 **卷积神经网络（CNN）** 分析模拟程序 **21cmFAST-VAO** 生成的宇宙黎明时期 21 cm **二维多频率角功率谱** 图像中的 **VAO 信号**。

CNN 可以估计出 **暗晕冷却阈值质量（M_cool）**。

## 文件说明

### 脚本

| 文件 | 说明 |
|------|------|
| `data.py` | 数据加载与预处理 |
| `count.py` | 文件计数统计 |
| `move.py` / `movecsv.py` | 文件移动工具 |
| `fixcsv.py` | CSV 数据修复 |
| `processnoise.py` | 噪声数据处理 |
| `probabilitydata.py` | 概率数据分析 |
| `VAOpic.py` | VAO 信号图像处理 |

### 笔记本

| 文件 | 说明 |
|------|------|
| `cnn_caseB.ipynb` | Case B 的 CNN 分析 |
| `cnn_caseC.ipynb` | Case C 的 CNN 分析 |

### 模型权重

| 文件 | 说明 |
|------|------|
| `best_model_caseB.pt` | Case B 最佳模型 |
| `best_model_caseC.pt` | Case C 最佳模型 |
| `cvmodelB/best_model_fold*.pt` | Case B 交叉验证模型（5 folds） |
| `cvmodelC/best_model_fold*.pt` | Case C 交叉验证模型（5 folds） |

### 数据子目录

| 目录 | 说明 |
|------|------|
| `dataNoise/` | 含噪声数据 |
| `dataNonoise/` | 无噪声数据 |
| `processed_tensors/caseB/` | Case B 预处理张量 |
| `processed_tensors/caseC/` | Case C 预处理张量 |
| `caseB/` | Case B 辅助脚本 |
| `caseC/` | Case C 辅助脚本 |
| `tmp/`、`tmp2/` | 临时脚本 |

## 背景

- **21cmFAST-VAO**: 模拟宇宙黎明时期 21 cm 信号的程序
- **二维多频率角功率谱**: 21 cm 信号在不同频率和角度上的涨落统计
- **VAO 信号**: 项目关注的特定天文信号特征
- **暗晕冷却阈值质量（M_cool）**: 暗晕能够冷却气体形成恒星的最小质量阈值
