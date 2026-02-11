import pandas as pd
import os 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from adjustText import adjust_text

# 定义文件路径
haplotype_input_file = 'C:/Users/LuzHu/Desktop/1.csv'  # 请替换为你的原始单倍群输入文件路径
processed_file = 'C:/Users/LuzHu/Desktop/PROCE.csv'
cumulative_file = 'C:/Users/LuzHu/Desktop/4大分区各级频率总表.csv'  # 请替换为分级单倍群频率输出文件路径
manhattan_input_file = cumulative_file  # 使用第一个代码生成的累加频率文件
manhattan_output_file = 'C:/Users/LuzHu/Desktop/曼哈顿图频率.csv'  # 指定群体的曼哈顿图频率差值结果

# 代码1：生成各级不同分类下的各级单倍群频率
def process_haplotype_data(input_file, output_file, cumulative_file_path):
    # 读取原始数据
    data = pd.read_csv(input_file)

    # 计算每个区域内的每个Haplotype的数量
    haplogroup_counts = data.groupby(['Haplotype', 'classification']).size().reset_index(name='count')

    # 创建数据透视表，将Haplotype作为行，区域作为列
    haplogroup_pivot = haplogroup_counts.pivot(index='Haplotype', columns='classification', values='count').fillna(0)

    # 计算每个区域内每个Haplotype的频率
    haplogroup_pivot = haplogroup_pivot.div(haplogroup_pivot.sum(axis=0), axis=1) * 100

    # 提取Haplotype列表并处理
    haplogroups = data['Haplotype'].tolist()
    processed_haplogroups = []

    # 按规则处理Haplotype
    for haplogroup in haplogroups:
        processed_haplogroups.append(haplogroup)
        while len(haplogroup) > 1:
            haplogroup = haplogroup[:-1]
            processed_haplogroups.append(haplogroup)

    # 去重并排序
    unique_processed_haplogroups = sorted(set(processed_haplogroups))

    # 创建包含处理后Haplotype的新DataFrame
    final_df = pd.DataFrame(unique_processed_haplogroups, columns=['Haplotype'])

    # 合并最终DataFrame和Haplotype频率DataFrame
    proce_df = final_df.merge(haplogroup_pivot, how='left', left_on='Haplotype', right_index=True).fillna(0)

    # 将结果保存到CSV文件
    proce_df.to_csv(output_file, index=False)

    # 清理数据类型
    df_cleaned = pd.read_csv(output_file)
    df_cleaned.iloc[:, 1:] = df_cleaned.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0)

    # 获取Haplotype列表
    haplogroups = df_cleaned['Haplotype'].tolist()

    # 初始化累加频率字典
    cumulative_freq = {col: {hg: 0 for hg in haplogroups} for col in df_cleaned.columns[1:]}

    # 定义检查Haplotype是否是另一个Haplotype下级的函数
    def is_descendant(parent, child):
        return child.startswith(parent) and len(child) > len(parent)

    # 缓存 is_descendant 结果
    descendant_cache = {}

    for parent in haplogroups:
        # 先处理 parent 自身的数据
        for col in df_cleaned.columns[1:]:
            if not df_cleaned.loc[df_cleaned['Haplotype'] == parent, col].empty:
                cumulative_freq[col][parent] += df_cleaned.loc[df_cleaned['Haplotype'] == parent, col].values[0]

        for child in haplogroups:
            if (parent, child) not in descendant_cache:
                descendant_cache[(parent, child)] = is_descendant(parent, child)
            if descendant_cache[(parent, child)]:
                for col in df_cleaned.columns[1:]:
                    if not df_cleaned.loc[df_cleaned['Haplotype'] == child, col].empty:
                        cumulative_freq[col][parent] += df_cleaned.loc[df_cleaned['Haplotype'] == child, col].values[0]

    # 创建存储累加频率的新DataFrame
    cumulative_df = pd.DataFrame(cumulative_freq).reset_index()
    cumulative_df.rename(columns={'index': 'Haplotype'}, inplace=True)

    # 将所有数值除以100
    cumulative_df.iloc[:, 1:] = cumulative_df.iloc[:, 1:] / 100

    # 保存累加频率到新文件
    cumulative_df.to_csv(cumulative_file_path, index=False)
    # 删除PROCE.csv
    os.remove(output_file)
    print("一个不需要的文件已经被删除了;\n累加后的文件路径：", cumulative_file_path)
    
    return cumulative_file_path

# 代码2部分
def data_transformation(input_file, output_file):
    # 读取输入文件
    df_input = pd.read_csv(input_file)

    # 创建输出文件的数据框架
    df_output = pd.DataFrame()

    # 第1列：SNP
    df_output['SNP'] = df_input.iloc[:, 0]

    # 第2列：CHR
    df_output['CHR'] = df_output['SNP'].str[0]

    # 第3列：POS
    df_output['POS'] = range(1, len(df_output) + 1)

    # 打印列名供用户选择
    print("可计算频率的群体列名如下：")
    print(df_input.columns)

    # 交互式输入被减数列名
    first_group_col = input("请输入第一个群体分类（被减数，输入列名）：")

    # 交互式输入减数列名
    second_group_col = input("请输入第二个群体分类（减数，输入列名）：")

    # 计算差值并填入第四列
    df_output['P'] = df_input[first_group_col] - df_input[second_group_col]

    # 保存结果到输出文件
    df_output.to_csv(output_file, index=False)

    print("该曼哈顿图的频率差值文件已保存，文件路径：", manhattan_output_file)
    return output_file, first_group_col, second_group_col

def plot_manhattan(file_path, title):
    # 设置字体类型
    rcParams['pdf.fonttype'] = 42
    rcParams['ps.fonttype'] = 42
    rcParams['font.sans-serif'] = ['Arial']
    
    # 读取数据
    mydata = pd.read_csv(file_path)

    # 提取绘图所需数据列
    chrom = mydata['CHR']
    pos = mydata['POS']
    pval = mydata['P']
    snp = mydata['SNP']

    # 设置颜色和形状
    colors = ['#EA1F1F', '#E88421', '#E5C923', '#ded82d', '#9DEF1B', '#42D726',
              '#449657', '#4CCCB3', '#369BA8', '#2B7EBC', '#3626D1', '#A128CE', '#999999']
    shapes = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'H', '+', 'x', 'd']

    # 设置阈值
    thresholds = [-0.05, 0.05]

    # 计算每个染色体的SNP数量和位置信息
    chrom_info = mydata.groupby('CHR')['POS'].agg(['min', 'max', 'count']).reset_index()
    chrom_info['width'] = chrom_info['max'] - chrom_info['min']

    # 绘制曼哈顿图
    plt.figure(figsize=(15, 5))

    # 分配每个染色体的X轴位置，避免重叠
    chrom_mapping = {}
    current_position = 0

    for _, row in chrom_info.iterrows():
        chrom = row['CHR']
        width = row['width']
        chrom_mapping[chrom] = current_position + width / 2
        current_position += width + 10  # 加上间隔避免重叠

    # 绘制点
    texts = []
    for chrom in chrom_mapping:
        group = mydata[mydata['CHR'] == chrom]
        x_base = chrom_mapping[chrom]
        x_positions = group['POS'] + (x_base - group['POS'].mean())  # 调整x位置使其分布在染色体中心
        y_positions = group['P']
        color = colors[list(chrom_mapping.keys()).index(chrom) % len(colors)]
        shape = shapes[list(chrom_mapping.keys()).index(chrom) % len(shapes)]
        plt.scatter(x_positions, y_positions, color=color, s=10, marker=shape)

        # 标记超过阈值的点并添加文字标签
        for (x, y, (_, row)) in zip(x_positions, y_positions, group.iterrows()):
            if row['P'] < thresholds[0] or row['P'] > thresholds[1]:
                text = plt.text(x, y, row['SNP'], fontsize=8, ha='right')
                texts.append(text)

    # 添加阈值线
    plt.axhline(y=thresholds[0], color='#999999', linestyle='--')
    plt.axhline(y=thresholds[1], color='#999999', linestyle='--')

    # 自动调整Y轴范围
    plt.ylim(pval.min() - 0.1, pval.max() + 0.1)

    # 调整文本位置以避免重叠并添加指向的线段
    adjust_text(texts, 
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.5, shrinkA=5),
                expand_text=(1.5, 1.5),
                expand_objects=(1.5, 1.5),
                force_text=(0.5, 0.5),
                force_objects=(0.5, 0.5),
                only_move={'points':'y', 'text':'xy'})

    # 设置X轴刻度和标签
    plt.xticks(ticks=[chrom_mapping[chrom] for chrom in chrom_mapping], labels=chrom_mapping.keys())
    plt.xlabel('Haplogroup')
    plt.ylabel('Frequency')
    plt.title(title)

    # 显示图像
    plt.show()

if __name__ == "__main__":
    # 处理Haplotype数据并生成累加频率文件
    cumulative_file = process_haplotype_data(haplotype_input_file, processed_file, cumulative_file)

    # 曼哈顿图绘制部分
    # 数据转换并生成曼哈顿图输入文件
    manhattan_output_file, first_group_col, second_group_col = data_transformation(cumulative_file, manhattan_output_file)

    # 使用生成的输出文件绘图，并设置图的标题为“列名1-列名2”
    plot_title = f"{first_group_col} - {second_group_col}"
    plot_manhattan(manhattan_output_file, plot_title)