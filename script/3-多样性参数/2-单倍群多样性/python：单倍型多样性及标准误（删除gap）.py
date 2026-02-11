from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# 设置字体属性，确保所有的文字都是可编辑的
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Arial'

# 文件路径
input_group_file = 'C:/Users/LuzHu/Desktop/1.txt'  # 群体信息文件
input_fasta_file = 'C:/Users/LuzHu/Desktop/Illumina_Y2206.fasta'  # 原始FASTA文件
output_fasta_dir = 'C:/Users/LuzHu/Desktop/cleaned_fasta_per_group/'  # 清理后的FASTA按群体存储的目录
output_diversity_file = 'C:/Users/LuzHu/Desktop/haplotype_diversity_results.csv'  # 多样性输出文件
output_lengths_file = 'C:/Users/LuzHu/Desktop/sequence_lengths_comparison.csv'  # 序列长度对比文件
output_plot_file = 'C:/Users/LuzHu/Desktop/haplotype_diversity_plot.pdf'  # 图表输出文件（PDF格式）

# 创建输出目录
os.makedirs(output_fasta_dir, exist_ok=True)

def create_color_gradient(start_color, mid1_color, mid2_color, end_color, steps):
    """
    创建颜色渐变。
    """
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
    加载群体信息文件，确保包含 'SampleID' 和 'Group' 列。
    """
    return pd.read_csv(group_file, sep='\t', header=0)

def load_fasta_file(fasta_file):
    """
    从FASTA文件加载序列数据。
    """
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append({'SampleID': record.id, 'Sequence': str(record.seq)})
    return pd.DataFrame(sequences)

def clean_fasta_per_group(group_data, sequence_data, output_dir):
    """
    按群体清理FASTA序列，删除每个群体中任何序列为'N'的所有位点。
    输出清理后的FASTA文件按群体存储，并返回清理前后长度对比。
    """
    merged_data = pd.merge(group_data, sequence_data, on='SampleID', how='inner')  # 合并群体和序列信息
    lengths_comparison = []

    for group, group_data in merged_data.groupby('Group'):
        print(f"Processing group: {group}")
        sequences = list(group_data['Sequence'])
        sequence_ids = list(group_data['SampleID'])

        # 转置序列矩阵（按位置分析）
        transposed = np.array([list(seq) for seq in sequences]).T
        non_n_positions = [i for i, column in enumerate(transposed) if 'N' not in column]  # 筛选没有N的位置

        # 清理后的序列
        cleaned_sequences = ["".join([seq[i] for i in non_n_positions]) for seq in sequences]

        # 保存清理结果
        cleaned_fasta_records = [
            SeqRecord(Seq(seq), id=seq_id, description="") for seq_id, seq in zip(sequence_ids, cleaned_sequences)
        ]
        group_fasta_path = os.path.join(output_dir, f"{group}_cleaned.fasta")
        SeqIO.write(cleaned_fasta_records, group_fasta_path, "fasta")
        print(f"Saved cleaned FASTA for group {group} to {group_fasta_path}")

        # 记录清理前后长度对比
        lengths_comparison.extend(
            [{'SampleID': seq_id, 'Group': group, 'Original_Length': len(sequences[0]), 'Cleaned_Length': len(seq)}
             for seq_id, seq in zip(sequence_ids, cleaned_sequences)]
        )

    return pd.DataFrame(lengths_comparison)

def assign_haplotypes(sequence_data):
    """
    分配单倍型。
    """
    sequence_data['Haplotype'] = sequence_data['Sequence'].rank(method='dense').astype(int)
    return sequence_data

def calculate_haplotype_diversity(data, group_col='Group', haplotype_col='Haplotype'):
    """
    计算单倍型多样性和标准误（Standard Error）。
    """
    diversity_results = []
    grouped = data.groupby(group_col)

    for group, group_data in grouped:
        n = len(group_data)  # 样本总数
        if n < 2:
            haplotype_diversity = None
            standard_error = None
        else:
            # 计算单倍型频率
            haplotype_counts = group_data[haplotype_col].value_counts()
            frequencies = haplotype_counts / n

            # 单倍型多样性公式
            sum_frequencies_squared = (frequencies ** 2).sum()
            haplotype_diversity = (n / (n - 1)) * (1 - sum_frequencies_squared)

            # 标准误公式
            standard_error = np.sqrt(np.sum(frequencies ** 2 * (1 - frequencies) ** 2) / (n * (n - 1)))

        diversity_results.append({
            'Group': group,
            'Haplotype_Diversity': haplotype_diversity,
            'Standard_Error': standard_error,  # 修改为 Standard Error
            'Sample_Size': n
        })

    return pd.DataFrame(diversity_results)


def plot_haplotype_diversity_dotplot_with_rectangles(diversity_results, output_plot_file):
    """
    绘制单倍型多样性图表（点 + 矩形误差条），将X轴表示群体，Y轴表示数值。
    按多样性值降序排列，并调整图表尺寸确保所有数据都可见。
    """
    diversity_results = diversity_results.dropna(subset=['Haplotype_Diversity', 'Standard_Error'])

    diversity_results = diversity_results.sort_values(by='Haplotype_Diversity', ascending=False)

    sorted_groups = diversity_results['Group']
    sorted_values = diversity_results['Haplotype_Diversity']
    sorted_errors = diversity_results['Standard_Error']

    min_error = 0.001
    adjusted_errors = sorted_errors.clip(lower=min_error)

    colors = create_color_gradient('#277571', '#8AAF7C', '#F3A262', '#E76F4F', len(sorted_groups))

    plt.figure(figsize=(max(12, len(sorted_groups) * 0.5), 6))

    for i, (group, value, error, color) in enumerate(zip(sorted_groups, sorted_values, adjusted_errors, colors)):
        plt.vlines(x=i, ymin=value - error, ymax=value + error, color=color, linewidth=5, alpha=0.8)
        plt.plot(i, value, 'o', color=color, markersize=8)

    for i, value in enumerate(sorted_values):
        plt.text(i, value + 0.01, f'{value:.4f}', va='bottom', ha='center', fontsize=8)

    plt.xlim(-1, len(sorted_groups))  # 增加 X 轴范围，留出空间
    plt.tight_layout(pad=3)  # 增加整体边距，防止边缘被截断
    plt.title('Haplotype Diversity with Rectangular Error Bars')
    plt.xlabel('Population')
    plt.ylabel('Haplotype Diversity')
    plt.xticks(range(len(sorted_groups)), sorted_groups, rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig(output_plot_file, format='pdf')
    plt.show()



# 主流程
group_data = load_group_file(input_group_file)
sequence_data = load_fasta_file(input_fasta_file)

lengths_comparison = clean_fasta_per_group(group_data, sequence_data, output_fasta_dir)
lengths_comparison.to_csv(output_lengths_file, index=False)

diversity_results_list = []

for group in lengths_comparison['Group'].unique():
    group_fasta_path = os.path.join(output_fasta_dir, f"{group}_cleaned.fasta")
    group_sequences = load_fasta_file(group_fasta_path)
    group_sequences['Group'] = group
    group_haplotype_data = assign_haplotypes(group_sequences)
    diversity_results = calculate_haplotype_diversity(group_haplotype_data)
    diversity_results_list.append(diversity_results)

final_diversity_results = pd.concat(diversity_results_list, ignore_index=True)
final_diversity_results.to_csv(output_diversity_file, index=False)

plot_haplotype_diversity_dotplot_with_rectangles(final_diversity_results, output_plot_file)

print("\nAnalysis completed successfully.")
