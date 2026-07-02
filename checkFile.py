#比较两个文件夹内文件是否一致

import os

def compare_folders(folder1, folder2):
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    
    only_in_folder1 = files1 - files2
    only_in_folder2 = files2 - files1
    
    print("仅在", folder1, "中的文件:")
    for file in sorted(only_in_folder1):
        print(file)
    
    print("\n仅在", folder2, "中的文件:")
    for file in sorted(only_in_folder2):
        print(file)

folder1 = "dataForLearning/202505/LW1"  # 替换为实际路径
folder2 = "dataForLearning/202505/LW2"  # 替换为实际路径
compare_folders(folder1, folder2)
