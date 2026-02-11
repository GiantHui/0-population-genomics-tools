# 导入所需的库
import pandas as pd
import numpy as np

# 载入数据，数据为CSV格式，编码为UTF-8
file_path = 'C:/Users/LuzHu/Desktop/15.csv' # 数据文件路径
save_path = 'C:/Users/LuzHu/Desktop/15Pro-Per归一化.csv' # 保存文件路径
data = pd.read_csv(file_path, encoding='utf-8')

# 将单倍群列设置为DataFrame的索引
data.set_index('Unnamed: 0', inplace=True)

# 定义计算共享单倍群矩阵的函数
def calculate_shared_haplogroups_matrix(haplogroups_data):
    # 获取人群数量
    n_populations = haplogroups_data.shape[1]
    # 初始化共享单倍群矩阵，初始值为0
    shared_haplogroups_matrix = np.zeros((n_populations, n_populations))
    
    # 获取人群名称列表
    populations = haplogroups_data.columns
    for i in range(n_populations):
        for j in range(i + 1, n_populations):
            # 计算两个人群之间共享单倍群的最小频率值
            shared_haplogroups = np.minimum(haplogroups_data[populations[i]], haplogroups_data[populations[j]])
            # 归一化共享单倍群的值
            shared_value = np.sum(shared_haplogroups) / (np.sum(haplogroups_data[populations[i]]) + np.sum(haplogroups_data[populations[j]]))
            shared_haplogroups_matrix[i, j] = shared_value
            shared_haplogroups_matrix[j, i] = shared_value
    
    # 将对角线的值设置为1，因为每个人群与自己的共享单倍群值是最大的
    np.fill_diagonal(shared_haplogroups_matrix, 1)
    
    # 返回一个新的DataFrame，其索引和列都是人群名称
    return pd.DataFrame(shared_haplogroups_matrix, index=populations, columns=populations)

# 使用函数计算共享单倍群矩阵
shared_matrix = calculate_shared_haplogroups_matrix(data)

# 输出计算得到的共享单倍群矩阵

with open(save_path, 'w', encoding='utf-8') as f:
    shared_matrix.to_csv(f)
    print('共享单倍群矩阵已经保存')

# 绘制热图
# df = pd.read_csv(save_path, encoding='utf-8',index_col=0)
# import seaborn as sns
# import matplotlib.pyplot as plt

# sns.heatmap(df, cmap='YlGnBu')
# plt.show()