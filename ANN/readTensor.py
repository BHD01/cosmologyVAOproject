import numpy as np

#读取.npy格式的张量文件

def load_tensor(file_path):
    """
    读取三维张量文件并返回数据。
    
    参数:
    file_path (str): .npy 文件的路径。
    
    返回:
    np.ndarray: 读取的三维张量。
    """
    try:
        # 加载张量数据
        tensor = np.load(file_path)
        print(f"Successfully loaded tensor with shape: {tensor.shape}")
        return tensor
    except Exception as e:
        print(f"Error loading tensor: {e}")
        return None

def display_tensor(tensor, max_slices=5):
    """
    显示三维张量中的具体数据。
    
    参数:
    tensor (np.ndarray): 三维张量。
    max_slices (int): 最大显示的切片数量。
    """
    if tensor is None:
        print("No tensor to display.")
        return
    
    # 获取张量形状
    num_slices, num_rows, num_cols = tensor.shape
    print(f"Tensor shape: {tensor.shape}")
    
    # 显示前几个切片的数据
    print(f"Displaying the first {min(max_slices, num_slices)} slices:")
    for i in range(min(max_slices, num_slices)):
        print(f"Slice {i + 1}:")
        print(tensor[i])
        print("-" * 40)

# 文件路径
file_path = input("请输入张量文件路径")  # 替换为实际路径

# 加载和显示数据
tensor = load_tensor(file_path)
display_tensor(tensor)
