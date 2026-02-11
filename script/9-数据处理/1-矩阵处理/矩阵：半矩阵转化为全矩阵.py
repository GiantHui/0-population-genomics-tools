import pandas as pd
import numpy as np

# 读取数据
file_path = 'C:/Users/LuzHu/Desktop/1.csv'  # 你的原始CSV文件路径
data = pd.read_csv(file_path, index_col=0, header=0)  # 第一列和第一行作为索引和列名

# 获取数据框的形状
n_rows, n_cols = data.shape

# 确保输入的是一个方阵
if n_rows != n_cols:
    raise ValueError("输入的CSV文件不是方阵！")

# 创建一个新的全矩阵，用来存储对称矩阵
full_matrix = data.copy()

# 遍历下三角部分，将数据镜像到上三角部分
for i in range(n_rows):
    for j in range(i + 1, n_cols):
        full_matrix.iat[i, j] = full_matrix.iat[j, i]  # 使用下三角部分的数据填充上三角部分
        full_matrix.iat[j, i] = full_matrix.iat[i, j]  # 使用上三角部分的数据填充下三角部分

# 保存生成的全矩阵到CSV文件
output_file_path = 'C:/Users/LuzHu/Desktop/level_tip.csv'
full_matrix.to_csv(output_file_path)

print("对称矩阵已成功保存到", output_file_path)
