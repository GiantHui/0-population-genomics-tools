from Bio import SeqIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 设置字体属性，确保所有的文字都是可编辑的
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Arial'

# 文件路径
input_group_file = 'C:/Users/LuzHu/Desktop/1.txt'  # 群体信息文件
input_fasta_file = 'C:/Users/LuzHu/Desktop/Illumina_Y2206.fasta'  # 序列文件
output_diversity_file = 'C:/Users/LuzHu/Desktop/haplotype_diversity_results.csv'  # 多样性输出文件
output_details_file = 'C:/Users/LuzHu/Desktop/haplotype_details.csv'  # 单倍型详情输出文件
output_plot_file = 'C:/Users/LuzHu/Desktop/haplotype_diversity_plot.pdf'  # 图表输出文件（PDF格式）

# 渐变颜色生成函数
def create_color_gradient(start_color, mid1_color, mid2_color, end_color, steps):
    colors_hex = [start_color, mid1_color, mid2_color, end_color]
    colors_rgb = [np.array([int(c[i:i+2], 16) for i in (1, 3, 5)]) / 255.0 for c in colors_hex]
    gradient = []

    for i in range(len(colors_rgb) - 1):
        start_rgb = colors_rgb[i]
        end_rgb = colors_rgb[i + 1]
        segment_steps = steps // (len(colors_rgb) - 1)
        for j in range(segment_steps):
            gradient.append(start_rgb + (end_rgb - start_rgb) * j / (segment_steps - 1))
    return [tuple(color) for color in gradient[:steps]]

def load_group_file(group_file):
    """
    加载群体文件。
    """
    return pd.read_csv(group_file, sep='\t', header=None, names=['SampleID', 'Group'])

def load_fasta_file(fasta_file):
    """
    加载fasta文件并提取序列。
    """
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append({'SampleID': record.id, 'Sequence': str(record.seq)})
    return pd.DataFrame(sequences)

def assign_haplotypes(sequence_data):
    """
    分配单倍型。
    """
    sequence_data['Haplotype'] = sequence_data['Sequence'].rank(method='dense').astype(int)
    return sequence_data

def calculate_haplotype_diversity(data, group_col='Group', haplotype_col='Haplotype'):
    """
    计算单倍型多样性，并统计单倍型数量和每种单倍型的样本数。
    """
    diversity_results = []
    haplotype_details = []  # 用于存储每个群体每种单倍型的样本数
    
    grouped = data.groupby(group_col)
    for group, group_data in grouped:
        n = len(group_data)
        if n < 2:
            haplotype_diversity = None
            standard_error = None
        else:
            # 统计每种单倍型的频率
            haplotype_counts = group_data[haplotype_col].value_counts()
            frequencies = haplotype_counts / n
            
            # 计算单倍型多样性
            sum_frequencies_squared = (frequencies ** 2).sum()
            haplotype_diversity = (n / (n - 1)) * (1 - sum_frequencies_squared)
            
            # 计算标准误差 (SE)
            standard_error = np.sqrt(np.sum(frequencies ** 2 * (1 - frequencies) ** 2) / (n - 1))
        
        # 统计单倍型数量
        haplotype_count = haplotype_counts.shape[0]
        
        # 保存单倍型详情
        for haplotype, count in haplotype_counts.items():
            haplotype_details.append({
                'Group': group,
                'Haplotype': haplotype,
                'Sample_Count': count
            })
        
        diversity_results.append({
            'Group': group,
            'Haplotype_Diversity': haplotype_diversity,
            'Standard_Error': standard_error,
            'Haplotype_Count': haplotype_count
        })
    
    # 转换结果为 DataFrame
    diversity_df = pd.DataFrame(diversity_results)
    haplotype_details_df = pd.DataFrame(haplotype_details)
    
    # 按多样性值降序排列
    diversity_df = diversity_df.sort_values(by='Haplotype_Diversity', ascending=False).reset_index(drop=True)
    
    return diversity_df, haplotype_details_df

def plot_haplotype_diversity_dotplot_with_rectangles(diversity_results, output_plot_file):
    """
    绘制单倍型多样性图表（点 + 矩形误差条），将X轴表示群体，Y轴表示数值。
    """
    # 确保数据无缺失
    diversity_results = diversity_results.dropna(subset=['Haplotype_Diversity', 'Standard_Error'])

    sorted_groups = diversity_results['Group']
    sorted_values = diversity_results['Haplotype_Diversity']
    sorted_errors = diversity_results['Standard_Error']
    
    # 设置误差条的最小显示值
    min_error = 0.001  # 确保误差条最小宽度足够可见
    adjusted_errors = sorted_errors.clip(lower=min_error)
    
    # 使用自定义颜色渐变
    colors = create_color_gradient('#277571', '#8AAF7C', '#F3A262', '#E76F4F', len(sorted_groups))
    
    # 创建图形
    plt.figure(figsize=(12, 6))
    
    for i, (group, value, error, color) in enumerate(zip(sorted_groups, sorted_values, adjusted_errors, colors)):
        # 绘制矩形误差条（用 vlines 模拟，垂直绘制）
        plt.vlines(x=i, ymin=value - error, ymax=value + error, color=color, linewidth=5, alpha=0.8)
        # 绘制点
        plt.plot(i, value, 'o', color=color, markersize=8)

    # 添加数值标签（保留四位小数）
    for i, value in enumerate(sorted_values):
        plt.text(i, value + 0.01, f'{value:.4f}', va='bottom', ha='center', fontsize=8)

    # 设置标题和轴标签
    plt.title('Haplotype Diversity with Rectangular Error Bars')
    plt.xlabel('Population')
    plt.ylabel('Haplotype Diversity')
    plt.xticks(range(len(sorted_groups)), sorted_groups, rotation=45, ha='right')  # X轴群体标签旋转

    # 调整布局
    plt.tight_layout()
    plt.savefig(output_plot_file, format='pdf')
    plt.show()


# 加载群体信息
group_data = load_group_file(input_group_file)

# 加载序列信息
sequence_data = load_fasta_file(input_fasta_file)

# 合并群体信息和序列信息
merged_data = pd.merge(group_data, sequence_data, on='SampleID')

# 分配单倍型
haplotype_data = assign_haplotypes(merged_data)

# 计算单倍型多样性及单倍型数量
diversity_results, haplotype_details = calculate_haplotype_diversity(haplotype_data)

# 保存结果到文件
diversity_results.to_csv(output_diversity_file, index=False)
haplotype_details.to_csv(output_details_file, index=False)

# 绘制图表并保存
plot_haplotype_diversity_dotplot_with_rectangles(diversity_results, output_plot_file)


