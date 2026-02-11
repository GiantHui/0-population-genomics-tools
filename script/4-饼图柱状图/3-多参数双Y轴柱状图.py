import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib

# ========== 设置字体 ==========
# 设置字体为可编辑，支持中文显示
matplotlib.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42  # 为了导出的PDF字体可编辑
plt.rcParams['ps.fonttype'] = 42  # 为了导出的PostScript文件字体可编辑

# ========== 设置路径 ==========
# 请在运行前根据实际文件路径修改以下变量
input_csv = "haplogroup_counts.csv"  # 输入：行为单倍群，列为群体，值为频数
expected_output_csv = "expected_frequencies.csv"  # 输出：期望频数表
output_plot = "haplogroup_composition_barplot.png"  # 输出：图片路径
output_statistical_results_csv = "statistical_results.csv"  # 输出：统计检验结果

# ========== 读取数据 ==========
# 假设 CSV 文件行为单倍群，列为群体，值为整数频数
df = pd.read_csv(input_csv, index_col=0)

# ========== 执行 χ² 检验 ==========
chi2_stat, chi2_p, chi2_dof, chi2_expected = stats.chi2_contingency(df, correction=False)
print("【χ² 检验】")
print(f"  χ² = {chi2_stat:.3f}, 自由度 = {chi2_dof}, 显著性 p = {chi2_p:.3e}")

# ========== 执行 G-test ==========
g_stat, g_p, g_dof, g_expected = stats.chi2_contingency(df, lambda_="log-likelihood")
print("\n【G 检验（对数似然）】")
print(f"  G = {g_stat:.3f}, 自由度 = {g_dof}, 显著性 p = {g_p:.3e}")

# ========== 导出期望频数 ==========
expected_df = pd.DataFrame(chi2_expected, index=df.index, columns=df.columns)
expected_df.to_csv(expected_output_csv)
print(f"\n期望频数表已保存为：{expected_output_csv}")

# ========== 统计学检验结果保存 ==========
# 创建一个包含 χ² 和 G-test 结果的 DataFrame
stat_results = pd.DataFrame({
    "χ² 统计量": [chi2_stat],
    "χ² 自由度": [chi2_dof],
    "χ² p值": [chi2_p],
    "G 统计量": [g_stat],
    "G 自由度": [g_dof],
    "G p值": [g_p]
})

# 将统计结果保存为 CSV 文件
stat_results.to_csv(output_statistical_results_csv, index=False)
print(f"统计检验结果已保存为：{output_statistical_results_csv}")

# ========== 频率可视化 ==========
# 将计数转换为频率
df_freq = df.div(df.sum(axis=0), axis=1)

# 绘图
plt.figure(figsize=(12, 6))
df_freq.T.plot(kind="bar", stacked=True, colormap="tab20", figsize=(12, 6), edgecolor='black')

plt.title("各群体单倍群频率组成", fontsize=16)
plt.ylabel("频率", fontsize=12)
plt.xlabel("群体", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="单倍群", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 保存堆叠柱状图
plt.savefig(output_plot, dpi=300)
print(f"堆叠柱状图已保存为：{output_plot}")

# 使用 matplotlib 的自带工具查看图像
plt.show()
