import pandas as pd
import numpy as np

# 输入和输出文件路径
input_file = '/mnt/c/Users/Administrator/Desktop/捕获体系散点图.txt'  # 替换为您的输入文件路径,有表头，表头中包含Latitude和Longitude
output_file = '/mnt/c/Users/Administrator/Desktop/捕获体系散点图偏移经纬度.txt'  # 替换为您想要的输出文件路径

# 读取数据
df = pd.read_csv(input_file, sep='\t')

# 定义偏移函数
def random_offset(lat, lon, delta=1.5):  # delta为偏移范围，可以自己设置，单位为度
    lat_offset = lat + np.random.uniform(-delta, delta)
    lon_offset = lon + np.random.uniform(-delta, delta)
    return lat_offset, lon_offset

# 应用偏移
df[['Latitude', 'Longitude']] = df.apply(lambda row: random_offset(row['Latitude'], row['Longitude']), axis=1, result_type='expand')

# 保存结果
df.to_csv(output_file, sep='\t', index=False)
