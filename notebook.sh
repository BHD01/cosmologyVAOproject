#!/bin/bash
#在服务器运行jupyter notebook
#SBATCH --job-name=jupyter
#SBATCH --partition=cpu           # GPU 分区名称
#SBATCH --nodelist=node3
#SBATCH --cpus-per-task=1        # 1 个 CPU 核心
#SBATCH --output=notebook_%j.log  # 日志文件
#SBATCH --error=job_error_%j.log       # 错误日志

# 激活 Conda 环境
source ~/.bashrc
conda activate dcos

# 获取分配的节点和端口
NODE=$(hostname)
PORT=$((RANDOM % 10000 + 10000))  # 随机端口（10000-20000）

# 启动 Jupyter Notebook
echo "Starting Jupyter Notebook on $NODE:$PORT"
jupyter notebook --no-browser --port=$PORT --ip=0.0.0.0 &

# 创建 SSH 隧道提示
echo "To access the Notebook, run on your local machine:"
echo "ssh -N -L $PORT:$NODE:$PORT duxi@10.0.10.80"

# 保持作业运行
wait