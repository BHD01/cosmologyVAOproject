#!/usr/bin/env bash
# 一个提交后不执行任何程序的脚本，用于远程连接某个无运行中作业的服务器节点

#SBATCH --job-name=notebook          # ��ҵ����
#SBATCH --output=job_output_%j.log      # ��׼�����־
#SBATCH --error=job_error_%j.log       # ������־
#SBATCH --nodelist=node[3]                # �������ƣ�����ʵ�����ѡ��
#SBATCH --nodes=1                      # ʹ��һ���ڵ�
#SBATCH --ntasks=1                     # һ������

while true
do
  sleep 10
done
