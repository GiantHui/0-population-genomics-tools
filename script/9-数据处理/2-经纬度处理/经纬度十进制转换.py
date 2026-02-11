import pandas as pd
import re

# ========== 配置部分 ==========
# 输入文件（CSV，逗号分隔）
INPUT_FILE = "/mnt/c/Users/Administrator/Desktop/1.csv"
# 输出文件
OUTPUT_FILE = "/mnt/c/Users/Administrator/Desktop/output.csv"
# ==============================

# 函数：将度分秒(DMS)格式转换为十进制度数
def dms_to_decimal(dms_str):
    """
    参数: dms_str (字符串) 如 "47°43'41.9\"N"
    返回: 十进制度数 (float)
    """
    # 使用正则表达式匹配 DMS 格式
    match = re.match(r"(\d+)°(\d+)'([\d.]+)\"?([NSEW])", dms_str.strip())
    if not match:
        raise ValueError(f"无法解析坐标: {dms_str}")
    degrees, minutes, seconds, direction = match.groups()
    degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    
    # 计算十进制度数
    decimal = degrees + minutes/60 + seconds/3600
    
    # 南纬(S)和西经(W)为负数
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# 读取输入 CSV（注意分隔符为逗号）
df = pd.read_csv(INPUT_FILE, sep=",")

# 转换纬度和经度，追加新列
df['Lat'] = df['GPSlatitude'].apply(dms_to_decimal)
df['Long'] = df['GPSlongitude'].apply(dms_to_decimal)

# 输出包含原始两列和新增两列
df_out = df[['GPSlatitude', 'GPSlongitude', 'Lat', 'Long']]

# 保存结果为新的 CSV 文件
df_out.to_csv(OUTPUT_FILE, index=False)

print(f"转换完成！结果已保存到 {OUTPUT_FILE}")
