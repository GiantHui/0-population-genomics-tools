import pandas as pd

# 载入数据
file_path = 'C:/Users/LuzHu/Desktop/level_tip.txt'
output_arp_file_path = 'C:/Users/LuzHu/Desktop/level_tip.arp'
data = pd.read_csv(file_path, delimiter='\t')

# Step 1: 为单倍群创建字典
unique_haplogroups = data['haplogroup'].unique()
hapl_dict = {haplogroup: idx + 1 for idx, haplogroup in enumerate(unique_haplogroups)}

# Step 2: 计算单倍群在人群中的出现频率
grouped_data = data.groupby(['name', 'haplogroup']).size().reset_index(name='count')

# Step 3: 生成样本频率文件
samples_file_content = ""
for group_name in grouped_data['name'].unique():
    group_data = grouped_data[grouped_data['name'] == group_name]
    sample_size = group_data['count'].sum()
    samples_block = f"\n\n\tSampleName=\"{group_name}\"\n\tSampleSize={sample_size}\n\tSampleData= {{\n"

    for haplogroup, idx in hapl_dict.items():
        count = group_data[group_data['haplogroup'] == haplogroup]['count'].sum()
        frequency = count / sample_size if sample_size > 0 else 0
        samples_block += f"\t\t{idx}\t{frequency:.6f}\n"

    samples_block += "\t}\n"
    samples_file_content += samples_block

# Step 4: 生成ARP文件头部内容
nb_samples = len(grouped_data['name'].unique())
profile_content = f"""[Profile]

    Title="The population fixation index(Fst) of Y-DNA"

    NbSamples={nb_samples}
    DataType=FREQUENCY
    GenotypicData=0
    LocusSeparator=' '
    MissingData="? "
    Frequency= REL
"""

# Step 5: 生成单倍群定义部分
hapl_list_content = "\n".join([f"{idx}\t{haplogroup}" for haplogroup, idx in hapl_dict.items()])

# Step 6: 合并所有内容为最终的Y-DNA.arp文件
combined_content = f'''{profile_content}\n
[Data]\n
[HaplotypeDefinition]\n
\tHaplList={{\n{hapl_list_content}}}\n
[Samples]\n{samples_file_content}'''

# Step 7: 写入最终的ARP文件
with open(output_arp_file_path, 'w') as example_arp_file:
    example_arp_file.write(combined_content)