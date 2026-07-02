#!/usr/bin/env bash
#在服务器运行python程序

#SBATCH --job-name=python          # 作业名称
#SBATCH --output=job_output_%j.log      # 标准输出日志
#SBATCH --error=job_error_%j.log       # 错误日志
#SBATCH --partition=amd                # 分区名称（根据实际情况选择）
#SBATCH --nodes=1                      # 使用一个节点
#SBATCH --ntasks=1                     # 一个任务
#SBATCH --cpus-per-task=4              # 每个任务使用 4 个 CPU 核心
#SBATCH --gres=gpu:1                   # 请求一个 GPU

# 设置 LD_PRELOAD 环境变量，指定 Conda 环境中的 libstdc++ 库
export LD_PRELOAD=~/.conda/envs/dcos/lib/libstdc++.so.6.0.29

# 激活 Python 环境
conda init bash
conda activate dcos


# 运行 Python 程序
python data.py
