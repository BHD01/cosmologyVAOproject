import os

# 定义主文件夹路径
base_path = "dataForLearning/Mcool"

# 遍历1.0到9.0的文件夹
for i in range(1, 21):
    folder_name = f"{i}"
    folder_path = os.path.join(base_path, folder_name)
    
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 获取文件夹内所有.csv文件
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        # 按照序号重命名文件
        for index, file_name in enumerate(csv_files, start=1):
            old_file_path = os.path.join(folder_path, file_name)
            new_file_name = f"{i}.0-{index}.csv"
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} -> {new_file_path}")
    else:
        print(f"Folder {folder_path} does not exist")