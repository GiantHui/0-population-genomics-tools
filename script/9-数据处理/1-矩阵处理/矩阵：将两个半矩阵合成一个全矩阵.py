import numpy as np

def read_matrix_from_csv(file_path):
    """
    从 CSV 文件读取矩阵
    :param file_path: 文件路径
    :return: 矩阵 (numpy.ndarray)
    """
    return np.genfromtxt(file_path, delimiter=',')  # 从 CSV 读取矩阵

def write_matrix_to_csv(matrix, file_path):
    """
    将矩阵写入 CSV 文件
    :param matrix: 要保存的矩阵 (numpy.ndarray)
    :param file_path: 文件路径
    """
    np.savetxt(file_path, matrix, delimiter=',', fmt="%s")  # 保存为 CSV 格式

def combine_half_matrices(lower_half, upper_half):
    """
    将左下半矩阵和右上半矩阵合并为一个全矩阵。
    :param lower_half: 左下半矩阵 (numpy.ndarray)
    :param upper_half: 右上半矩阵 (numpy.ndarray)
    :return: 合成后的全矩阵 (numpy.ndarray)
    """
    # 检查输入矩阵的维度
    n = lower_half.shape[0]
    assert lower_half.shape == (n, n), "左下半矩阵必须是 n x n 的方阵"
    assert upper_half.shape == (n, n), "右上半矩阵必须是 n x n 的方阵"

    # 创建全矩阵
    full_matrix = np.zeros((n, n), dtype=lower_half.dtype)

    # 填充左下半部分
    for i in range(n):
        for j in range(i + 1):
            full_matrix[i, j] = lower_half[i, j]

    # 填充右上半部分
    for i in range(n):
        for j in range(i, n):
            full_matrix[i, j] = upper_half[i, j]

    return full_matrix

# 文件路径
lower_half_file = "C:/Users/LuzHu/Desktop/1.csv"  # 替换为左下半矩阵的文件路径
upper_half_file = "C:/Users/LuzHu/Desktop/2.csv"  # 替换为右上半矩阵的文件路径
output_file = "C:/Users/LuzHu/Desktop/3.csv"  # 合成矩阵的输出文件路径

# 读取矩阵
lower_half = read_matrix_from_csv(lower_half_file)
upper_half = read_matrix_from_csv(upper_half_file)

# 合成全矩阵
full_matrix = combine_half_matrices(lower_half, upper_half)

# 将结果保存为 CSV 文件
write_matrix_to_csv(full_matrix, output_file)

print(f"合成的全矩阵已保存到 {output_file}")
