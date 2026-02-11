
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal

# 读取数据
file_path = 'C:/Users/Administrator/Desktop/1.txt'
output_file_path = 'C:/Users/Administrator/Desktop/City_terminal_hg.csv'
data = pd.read_csv(file_path, sep='\t')

# 分组并计算每个群体的单倍型多样性
diversities = []
group_sizes = data['Population_Province'].value_counts()

for group, group_data in data.groupby('Population_Province'):
    n = len(group_data)
    if n >= 10:
        haplotype_counts = group_data['Haplo'].value_counts()
        haplotype_frequencies = haplotype_counts / n
        HD = n * (1 - sum(haplotype_frequencies**2)) / (n - 1)
        diversities.append((group, HD, n))

# 转为DataFrame
diversity_df = pd.DataFrame(diversities, columns=['Group', 'Haplotype Diversity', 'Sample Size'])

# 统计学检验
groups = diversity_df['Group'].unique()
group_data = [diversity_df[diversity_df['Group'] == group]['Haplotype Diversity'].values for group in groups]
stat, p = kruskal(*group_data)

# 输出统计学检验结果
print(f"Kruskal-Wallis H检验结果: H-statistic = {stat}, p-value = {p}")

# 保存结果到CSV文件
with open(output_file_path, 'w') as f:
    f.write(f"Kruskal-Wallis H检验结果: H-statistic = {stat}, p-value = {p}\n")
diversity_df.to_csv(output_file_path, mode='a', index=False)

# 排序数据
diversity_df = diversity_df.sort_values(by='Haplotype Diversity')

# 添加群体数量到群体名称
diversity_df['Group'] = diversity_df.apply(lambda row: f"{row['Group']} ({row['Sample Size']})", axis=1)

# 可视化结果：柱状图
plt.figure(figsize=(14, 7))
sns.barplot(x='Group', y='Haplotype Diversity', data=diversity_df, palette='hsv')
plt.xlabel('Group')
plt.ylabel('Haplotype Diversity')
plt.title('Haplotype Diversity of Different Groups')
plt.xticks(rotation=90)  # 群体名称旋转90度便于阅读
plt.tight_layout()

# 展示图表
plt.show()

# 可选：保存图表
# output_chart_path = 'group_haplotype_diversities_barplot.png'
# plt.savefig(output_chart_path)
