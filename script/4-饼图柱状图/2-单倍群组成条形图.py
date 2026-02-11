import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 设置 rcParams 以确保导出的图表是可编辑的
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 加载数据
file_path = 'C:/Users/LuzHu/Desktop/1.txt'
data = pd.read_csv(file_path, sep='\t')

# 定义一个函数以生成更多颜色（如果需要）
def generate_colors(num_colors):
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_colors > len(colors):
        # 如果需要更多颜色，则使用颜色映射生成它们
        colormap = plt.get_cmap('hsv', num_colors)
        colors = [colormap(i) for i in range(num_colors)]
    return colors

# 删除非数值列以便进行绘图
plot_data = data.select_dtypes(include=['float64', 'int64'])

# 检查是否存在 Population 列，并将其设置为索引
if 'Population' in data.columns:
    plot_data.index = data['Population']
else:
    raise ValueError("The 'Population' column is missing from the data.")

# 确定属性的数量
num_attributes = len(plot_data.columns)

# 生成所需数量的颜色
colors = generate_colors(num_attributes)

# 绘制堆积条形图并应用新的颜色
plt.figure(figsize=(12, 8))
plot_data.plot(kind='bar', stacked=True, color=colors)
plt.title('Stacked Bar Chart with Generated Colors')
plt.xlabel('Population')
plt.ylabel('Values')
plt.legend(title='Attributes', bbox_to_anchor=(1.05, 1), loc='upper left')

# 显示图表
plt.show()

