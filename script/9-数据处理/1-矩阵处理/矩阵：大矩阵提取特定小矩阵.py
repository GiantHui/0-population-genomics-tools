import pandas as pd

# 读取CSV文件
file_path = 'C:/Users/LuzHu/Desktop/处理后Fst.csv'  # 替换为你的文件路径
fst_matrix = pd.read_csv(file_path)

# 交互式输入待提取的行
print("请输入要提取的行名称，多个名称之间用逗号或空格分隔:")
rows_input = input()
rows_to_extract = [row.strip() for row in rows_input.replace(',', ' ').split()]

# 交互式输入待提取的列
print("请输入要提取的列名称，多个名称之间用逗号或空格分隔:")
columns_input = input()
columns_to_extract = [col.strip() for col in columns_input.replace(',', ' ').split()]

# 提取指定行和列
fst_subset = fst_matrix.set_index('Unnamed: 0').loc[rows_to_extract, columns_to_extract]

# 保存矩阵结果为第一个输出文件
output_file_path_matrix = 'C:/Users/LuzHu/Desktop/所有汉_所有少fst_matrix.csv'  # 输出文件路径
fst_subset.to_csv(output_file_path_matrix)
print(f"子矩阵已保存至 {output_file_path_matrix}")

# 构建第二个输出的数据格式
result_list = [
    (f"{row} vs {col}", fst_subset.loc[row, col])
    for row in fst_subset.index
    for col in fst_subset.columns
]

# 将结果保存为第二个输出文件
output_file_path_pairs = 'C:/Users/LuzHu/Desktop/所有汉_所有少fst_pairs.txt'  # 输出文件路径
with open(output_file_path_pairs, 'w') as f:
    for pair, value in result_list:
        f.write(f"{pair}\t{value}\n")

print(f"行列值对已保存至 {output_file_path_pairs}")
