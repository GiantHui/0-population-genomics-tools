import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 文件路径
file_path = '/mnt/c/Users/Administrator/Desktop/Fu.FS不显著.txt'

# 设置字体属性，确保所有的文字都是可编辑的
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'Arial'

# 读取数据文件，并处理空行和格式问题
def read_data_from_txt(file_path):
    groups, values, significances = [], [], []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # 跳过表头
            if line.strip():  # 跳过空行
                parts = line.strip().split()
                if len(parts) >= 3:  # 确保有三列数据
                    group, value, significance = parts[0], float(parts[1]), float(parts[2])
                    groups.append(group)
                    values.append(value)
                    significances.append(significance)
    return groups, values, significances

# 选项：是否按 Y 轴值大小排序
sort_by_value = True  # 设置为 False 则保持输入顺序不变

# 从文件中读取数据
groups, values, significances = read_data_from_txt(file_path)

if sort_by_value:
    # 按数据值进行排序（从高到低）
    sorted_data = sorted(zip(groups, values, significances), key=lambda x: x[1], reverse=True)
    sorted_groups, sorted_values, sorted_significances = zip(*sorted_data)
else:
    # 保持原始顺序
    sorted_groups, sorted_values, sorted_significances = groups, values, significances

# 绘制折线图
fig, ax1 = plt.subplots(figsize=(14, 6))  # 调整图形宽度为14

# 绘制数据值
ax1.plot(sorted_groups, sorted_values, '-o', color='#277571')
ax1.set_xlabel('Time')
ax1.set_ylabel('FS', color='#277571')
ax1.tick_params(axis='y', labelcolor='#277571')

# 创建一个共享X轴的第二个Y轴
ax2 = ax1.twinx()
ax2.plot(sorted_groups, sorted_significances, '-o', color='#E76F4F')
ax2.set_ylabel('P value', color='#E76F4F')
ax2.tick_params(axis='y', labelcolor='#E76F4F')

# 设置标题
plt.title('Line Plot with Dual Axis')

# 设置X轴标签及旋转
ax1.set_xticks(range(len(sorted_groups)))
ax1.set_xticklabels(sorted_groups, rotation=45, ha='right', fontsize=10)

# 调整图形布局
plt.tight_layout()

# 显示图表
plt.show()
