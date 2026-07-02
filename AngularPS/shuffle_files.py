import os
import random
import shutil

def shuffle_and_redistribute_files(folder1, folder2, folder3):
    # 获取所有文件夹中的文件列表
    files1 = [os.path.join(folder1, f) for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
    files2 = [os.path.join(folder2, f) for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]
    files3 = [os.path.join(folder3, f) for f in os.listdir(folder3) if os.path.isfile(os.path.join(folder3, f))]
    
    # 记录原始文件数量
    count1, count2, count3 = len(files1), len(files2), len(files3)
    
    # 合并所有文件
    all_files = files1 + files2 + files3
    
    # 打乱文件列表
    random.shuffle(all_files)
    
    # 创建临时文件夹用于文件移动
    temp_dir = "temp_shuffle"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 将所有文件移动到临时文件夹
        for file_path in all_files:
            shutil.move(file_path, os.path.join(temp_dir, os.path.basename(file_path)))
        
        # 获取临时文件夹中的文件列表
        temp_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
        
        # 重新分配文件
        for i, file_path in enumerate(temp_files):
            if i < count1:
                shutil.move(file_path, os.path.join(folder1, os.path.basename(file_path)))
            elif i < count1 + count2:
                shutil.move(file_path, os.path.join(folder2, os.path.basename(file_path)))
            else:
                shutil.move(file_path, os.path.join(folder3, os.path.basename(file_path)))
    
    finally:
        # 清理临时文件夹
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# 使用示例
if __name__ == "__main__":
    data_for_learning = "dataForLearning/Mcool"
    data_for_testing = "dataForTesting/Mcool"
    data_for_validation = "dataForValidation/Mcool"
    
    shuffle_and_redistribute_files(data_for_learning, data_for_testing, data_for_validation)
    print("文件已重新分配完成")