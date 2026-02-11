import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 从Excel导入数据
file_path = "C:/Users/Administrator/Desktop/Continent_language_neutral.xlsx"  # 使用原始字符串路径
df = pd.read_excel(file_path)

# 确保数据列名与脚本一致
df.columns = ['Populations', 'mt_Tajima’s D', 'mt_p_value', 'Y_Tajima’s D', 'Y_p_value']

# 从txt文件中读取Y轴排序顺序
txt_file_path = "C:/Users/Administrator/Desktop/显示顺序.txt"  # 替换为实际路径
with open(txt_file_path, 'r') as f:
    population_order = [line.strip() for line in f.readlines()]

# 按照txt文件中的顺序调整Y轴
df_sorted = df.set_index('Populations').reindex(population_order).reset_index()

# 设置图形大小
plt.figure(figsize=(14, 12))  # 调整图形的宽度与高度，交换长宽比

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 创建纯色渐变颜色映射
cmap_mt = LinearSegmentedColormap.from_list("BlueGradient", ["#0D47A1","#1976D2", "#2196F3", "#64B5F6", "#BBDEFB"])
cmap_y = LinearSegmentedColormap.from_list("GreenGradient", ["#004D40","#00796B", "#009688", "#4DB6AC", "#B2DFDB"])

# 绘制第一种遗传标记的散点图（mtDNA），使用圆形标记，去掉边缘
scatter_mt = plt.scatter(
    df_sorted['Populations'],  # 将X轴和Y轴数据互换
    df_sorted['mt_Tajima’s D'],  # Y轴使用Tajima's D
    c=df_sorted['mt_p_value'], 
    cmap=cmap_mt, 
    marker='o', 
    label='Tajima’s D of mtDNA', 
    s=60,  # 点的大小
    alpha=0.8,
    edgecolor='none'  # 去掉边缘
)

# 绘制第二种遗传标记的散点图（Y染色体），使用三角形标记，去掉边缘
scatter_y = plt.scatter(
    df_sorted['Populations'],  # 将X轴和Y轴数据互换
    df_sorted['Y_Tajima’s D'],  # Y轴使用Tajima's D
    c=df_sorted['Y_p_value'], 
    cmap=cmap_y, 
    marker='^',  # 三角形标记
    label='Tajima’s D of Y chromosome', 
    s=60,  # 点的大小
    alpha=0.8,
    edgecolor='none'  # 去掉边缘
)

# 添加图表信息
plt.ylabel('Mean Pairwise Distance (Tajima’s D)', fontsize=10, fontname='Arial')  # Y轴标签
plt.xlabel('Populations', fontsize=10, fontname='Arial')  # X轴标签
plt.title('Comparison of Tajima’s D value for Y chromosome and mtDNA', fontsize=12)

# 调整X轴刻度标签字体大小
plt.tick_params(axis='x', labelsize=8)  # 设置X轴刻度标签的字体大小为8
plt.xticks(rotation=90)
# 添加图例，调整字体大小和标记的大小
plt.legend(fontsize=8, markerscale=0.8)

# 添加颜色条以显示p值的渐变，调整颜色条大小
# 创建一个新轴用于颜色条，将其放在右上角
cbar_ax_mt = plt.gca().inset_axes([0.8, 0.85, 0.03, 0.15])  # 设置颜色条位置
cbar_mt = plt.colorbar(scatter_mt, cax=cbar_ax_mt, label='P-value for mtDNA', shrink=0.6)

cbar_ax_y = plt.gca().inset_axes([0.8, 0.6, 0.03, 0.15])  # Y染色体的颜色条
cbar_y = plt.colorbar(scatter_y, cax=cbar_ax_y, label='P-value for Y chromosome', shrink=0.6)

# 添加网格线
plt.grid(axis='y', linestyle='--', alpha=0.6)

# 确保布局紧凑
plt.tight_layout()

# 保存为PDF文件，确保文本可编辑
pdf_output_path = "C:/Users/Administrator/Desktop/Continent_language_neutral.pdf"  # 输出PDF路径
plt.savefig(pdf_output_path, format='pdf', bbox_inches='tight')

# 显示图形
plt.show()
