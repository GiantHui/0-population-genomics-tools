import pandas as pd
import numpy as np

# 读取数据
file_path = 'C:/Users/LuzHu/Desktop/1.csv'  # 你的原始CSV文件路径
data = pd.read_csv(file_path, index_col=0)  # 假设第一列为索引

# 获取数据框的形状
n_rows, n_cols = data.shape

# 确保是方阵
if n_rows != n_cols:
    raise ValueError("The input CSV file is not a square matrix!")

# 删除对角线和右上三角数据
for i in range(n_rows):
    for j in range(i, n_cols):  # 从i开始，包括对角线
        data.iat[i, j] = np.nan  # 使用np.nan来替代None删除数据

# 删除对角线上的0（假设对角线上都是0）
np.fill_diagonal(data.values, np.nan)

# 保存修改后的数据到CSV
output_file_path = 'C:/Users/LuzHu/Desktop/2.csv'  # 你的输出CSV文件路径
data.to_csv(output_file_path)
