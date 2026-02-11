import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import mannwhitneyu, ttest_ind
import os
import matplotlib

# 确保字体可编辑
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Arial'  # 设置字体

# 读取数据
file_path = "/mnt/c/Users/Administrator/Desktop/test.txt"
data = pd.read_csv(file_path, sep="\t")

# 输出文件目录
outliers_file_path = os.path.join(os.path.dirname(file_path), "C:/Users/LuzHu/Desktop/O2a_outliers.csv")
output_file_path = os.path.join(os.path.dirname(file_path), "C:/Users/LuzHu/Desktop/O2a_comparisons.csv")

# 转为长格式（适合绘图）
data_melted = data.melt(var_name='Group', value_name='Fst').dropna()

# 定义颜色调色板
palette = sns.color_palette("Set3", len(data.columns))

# 创建图像
plt.figure(figsize=(15, 8))
ax = sns.boxplot(x='Group', y='Fst', data=data_melted, palette=palette)

# 设置标题和标签
plt.title('O2a', fontsize=16, weight='bold', pad=20)
plt.xlabel('Group', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# 函数：根据 p 值返回星号数量
def get_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'ns'  # Not significant

# 记录显著性结果（Mann-Whitney U 和 Welch t 检验）
group_names = data.columns
significance_results = []

for i, (group1, group2) in enumerate(combinations(group_names, 2)):
    group1_values = data[group1].dropna()
    group2_values = data[group2].dropna()
    
    stat_u, p_u = mannwhitneyu(group1_values, group2_values)
    stat_t, p_t = ttest_ind(group1_values, group2_values, equal_var=False)

    significant = 'significant' if p_u < 0.05 and p_t < 0.05 else 'not significant'

    result = {
        'id': f"Group{i + 1}",
        'group1': group1,
        'group2': group2,
        'U-statistic': stat_u,
        'p-value (U)': p_u,
        't-statistic (Welch)': stat_t,
        'p-value (Welch)': p_t,
        'significance': significant
    }
    significance_results.append(result)

# 输出显著性结果
print("两种检验均显著的组及其 p 值：")
for result in significance_results:
    if result['significance'] == 'significant':
        print(f"{result['id']} ({result['group1']} vs {result['group2']}): "
              f"U-statistic={result['U-statistic']:.4f}, p-value (U)={result['p-value (U)']:.4e}, "
              f"t-statistic (Welch)={result['t-statistic (Welch)']:.4f}, p-value (Welch)={result['p-value (Welch)']:.4e}")

# 交互：选择想要标注的组
user_input = input("请输入想要显示的组别代号，用逗号隔开（如：'Group1,Group2'）：")
selected_ids = [comp.strip() for comp in user_input.split(",")]

# 设置标注的偏移量
y_offset = 0.02
line_offset = 0.05

# 绘制显著性标注
for i, result in enumerate(significance_results):
    if result['id'] in selected_ids:
        group1, group2 = result['group1'], result['group2']
        x1, x2 = group_names.get_loc(group1), group_names.get_loc(group2)

        # 设置显著性标注的高度
        y, h = data_melted['Fst'].max() + y_offset + i * line_offset, line_offset
        ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, color='black')

        # 显示显著性标记（无框）
        ax.text((x1 + x2) / 2, y + h, get_stars(result['p-value (U)']),
                ha='center', va='bottom',
                fontsize=12)

# 保存显著性结果到 CSV
result_df = pd.DataFrame(significance_results)
result_df.to_csv(output_file_path, index=False)

# 找出每个组的离群值
outliers = []

for group in data.columns:
    group_values = data[group].dropna()
    q1 = group_values.quantile(0.25)
    q3 = group_values.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    group_outliers = group_values[(group_values < lower_bound) | (group_values > upper_bound)]
    for value in group_outliers:
        outliers.append({'Group': group, 'Outlier': value})

# 保存离群值到 CSV
outliers_df = pd.DataFrame(outliers)
outliers_df.to_csv(outliers_file_path, index=False)

# 显示图表
plt.show()

print(f"比较结果已保存至: {output_file_path}")
print(f"离群值已保存至: {outliers_file_path}")
