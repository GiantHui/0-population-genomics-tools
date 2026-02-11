
# Re-importing the necessary library as the code execution state has been reset.
import pandas as pd

# 替换这个txt分组文件
file_path = '/mnt/c/Users/Administrator/Desktop/民族.txt'

# Read the file into a pandas DataFrame
group_data = pd.read_csv(file_path, sep="\t", header=None, names=["ID", "Category"])

# Group the IDs by category
grouped = group_data.groupby('Category')['ID'].apply(list).to_dict()

# Start writing the content for the .arp file
arp_content = "[[Structure]]\n\n"
arp_content += 'StructureName="New Edited Structure"\n'
arp_content += f'NbGroups={len(grouped)}\n\n'

# Loop through each category and add its IDs to the content
for category, IDs in grouped.items():
    arp_content += f'Group={{\n'
    for ID in IDs:
        arp_content += f'\t"{ID}"\n'
    arp_content += "}\n.......\n"

# 替换输出的文件
arp_file_path = '/mnt/c/Users/Administrator/Desktop/民族.arp'

# Write the content to the new .arp file
with open(arp_file_path, 'w', encoding='utf-8') as arp_file:
    arp_file.write(arp_content)

arp_file_path