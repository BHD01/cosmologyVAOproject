import os
import random
#从模拟功率谱中抽取验证集
#需要先提取完测试集再执行这项任务

def random_sample_files(folder_path, sample_size=10):
    """
    从指定文件夹中随机抽取指定数量的文件
    
    参数:
        folder_path (str): 文件夹路径
        sample_size (int): 要抽取的文件数量，默认为10
        
    返回:
        list: 随机抽取的文件名列表
    """
    # 获取文件夹中所有文件
    all_files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f))]
    
    # 检查文件数量是否足够
    if len(all_files) < sample_size:
        raise ValueError(f"文件夹中只有 {len(all_files)} 个文件，少于要求的 {sample_size} 个")
    
    # 随机抽取文件
    sampled_files = random.sample(all_files, sample_size)
    
    return sampled_files

# 使用示例
if __name__ == "__main__":
    folder = "dataForLearning/202505L"  # 替换为你的文件夹路径
    try:
        selected_files = random_sample_files(folder)
        print("随机抽取的文件:")
        for file in selected_files:
            print(file)
    except Exception as e:
        print(f"发生错误: {e}")