import pandas as pd
import os 
# 读取原始数据
file_path = 'C:/Users/LuzHu/Desktop/少数民族原始.csv'  # 请替换为你的文件路径
data = pd.read_csv(file_path)

# 计算每个区域内的每个Haplotype的数量
haplogroup_counts = data.groupby(['Haplotype', 'Classfication']).size().reset_index(name='count')

# 创建数据透视表，将Haplotype作为行，区域作为列
haplogroup_pivot = haplogroup_counts.pivot(index='Haplotype', columns='Classfication', values='count').fillna(0)

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
proce_df.to_csv('./PROCE.csv', index=False)
df_cleaned = pd.read_csv('./PROCE.csv')

# 将频率列转换为数值类型
df_cleaned.iloc[:, 1:] = df_cleaned.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0)

# 获取Haplotype列表
haplogroups = df_cleaned['Haplotype'].tolist()

# 初始化累加频率字典
cumulative_freq = {col: {hg: 0 for hg in haplogroups} for col in df_cleaned.columns[1:]}

# 定义检查Haplotype是否是另一个Haplotype下级的函数
def is_descendant(parent, child):
    return child.startswith(parent) and len(child) > len(parent)

# 假设 is_descendant 函数和 haplogroups, df_cleaned, cumulative_freq 数据框已定义

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

# 保存累加频率到新文件
cumulative_file_path = 'C:/Users/LuzHu/Desktop/各级Haplotype频率总表累计.csv'
cumulative_df.to_csv(cumulative_file_path, index=False)
# 删除PROCE.csv
os.remove('./PROCE.csv')
print("一个不需要的文件已经被删除了;\n累加后的文件路径：", cumulative_file_path)