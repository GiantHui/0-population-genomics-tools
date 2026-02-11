# -*- coding: utf-8 -*-
"""
功能:
    1. 读取一个带表头的txt文件, 第一列为X轴参数(如 length, gap 等),
       后续列为不同序列数据;
    2. 提供两个模式:
        (a) 对所有数值进行 /1e6 转换, 并以 Mb 计量
        (b) 直接使用原始数值, 不做任何转换
    3. 只使用一个Y轴, 并根据数据范围自动或手动设置Y轴上限;
    4. 绘制分组柱状图, X轴为各行参数, 不同列序列并排显示;
    5. 可以旋转 X 轴标签, 使其竖排显示.

使用方法:
    1. 修改 `input_file` 路径以指向你的txt文件;
    2. 通过“convert_to_mb”变量(或注释代码块)决定是否转换为Mb;
    3. 运行脚本, 自动解析并绘制分组柱状图.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#==================在此处修改输入文件路径==================#
input_file = "C:/Users/Administrator/Desktop/Continent_lagua.txt"

#==================在此处可手动设置Y轴范围==================#
manual_ymin = 0      # Y轴最小值
manual_ymax = None   # 若需要手动指定上限, 填写数值, 否则留None自动计算

#==================在此处选择是否转换为 Mb==================#
# 若为True, 则对数据除以1e6并在Y轴标签中显示"(Mb)"
# 若为False, 则保留原始数据, Y轴标签为"Value"
convert_to_mb = False
#========================================================#

#==================设置字体与字符==================#
matplotlib.rcParams['font.sans-serif'] = ['Arial']  # 可换成 'SimHei', 'Microsoft YaHei' 等
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

#==================自定义柱状图颜色==================#
colors = [
    "#4B93E2", "#79C765", "#D66733", "#F2BE54", "#B977B9",
    "#FF7F50", "#8FBC8F", "#DC143C", "#708090", "#FFD700"
]
#==================================================#

# 1. 读取 txt 文件
x_labels = []   # 每行的参数名(第一列)
data_list = []  # 每行的数据(其余列)
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [ln.strip() for ln in f if ln.strip()]
    if len(lines) < 2:
        raise ValueError("输入文件至少需要包含表头和一行数据!")
    # 读取表头
    header = lines[0].split()
    series_labels = header[1:]  # 除去第一列(参数名), 剩下是各序列标签

    # 读取数据行
    for line in lines[1:]:
        parts = line.split()
        x_labels.append(parts[0])         # 该行的名称(显示在X轴)
        raw_values = [float(val) for val in parts[1:]]
        # 根据标记决定是否转换为 Mb
        if convert_to_mb:
            converted_values = [v / 1e6 for v in raw_values]
            data_list.append(converted_values)
        else:
            data_list.append(raw_values)

num_groups = len(x_labels)       # X轴分组数量
num_series = len(series_labels)  # 每个分组里有多少柱子(列数)
if num_groups == 0 or num_series == 0:
    raise ValueError("txt数据不完整或有误!")

# 2. 准备 X 轴位置, 让各序列并排显示
x = np.arange(num_groups)
bar_width = 0.8 / num_series
offset_mid = bar_width * (num_series - 1) / 2

# 3. 创建画布与坐标轴(单Y轴)
fig, ax = plt.subplots(figsize=(8, 4))

# 4. 绘制分组柱状图
bar_handles = {}
for row_i in range(num_groups):
    for col_i in range(num_series):
        offset = col_i * bar_width
        bar_container = ax.bar(
            x[row_i] + offset,
            data_list[row_i][col_i],
            bar_width,
            color=colors[col_i % len(colors)],
            label=series_labels[col_i] if row_i == 0 else ""
        )
        # 只在第一行(row_i=0)时设置图例
        if row_i == 0:
            bar_handles[col_i] = bar_container

#==================在此处修改坐标轴标签==================#
ax.set_xticks(x + offset_mid)
# 将X轴标签旋转90°, 如果不需要可以改成 rotation=0
ax.set_xticklabels(x_labels, rotation=90)

# 如果选择转换为Mb, 则Y轴标签加上(Mb), 否则写成Value
if convert_to_mb:
    ax.set_ylabel("Value (Mb)", fontsize=12)
else:
    ax.set_ylabel("Value", fontsize=12)

ax.set_xlabel("Parameter", fontsize=12)
#=====================================================#

# 5. 自动/手动设置Y轴范围
all_values = [val for row in data_list for val in row]
max_val = max(all_values)
if manual_ymax is not None:
    ymax = manual_ymax
else:
    ymax = max_val * 1.2
ax.set_ylim(manual_ymin, ymax)

# 6. 合并图例并显示
legend_handles = [bar_handles[c][0] for c in range(num_series)]
ax.legend(legend_handles, series_labels, loc='best')

plt.tight_layout()
plt.show()
