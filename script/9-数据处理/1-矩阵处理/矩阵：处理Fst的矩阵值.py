import pandas as pd

# 读取两张表
df1 = pd.read_csv('C:/Users/LuzHu/Desktop/表1.csv')
df2 = pd.read_csv('C:/Users/LuzHu/Desktop/表2.csv')

# 确保两张表的形状相同
if df1.shape != df2.shape:
    raise ValueError("两张表的形状不相同，无法处理。")

# 在第一张表有内容的位置保留第二张表的值，否则删除第二张表对应位置的内容
df_result = df2.where(df1.notna(), other=None)

# 保存结果到新CSV文件
df_result.to_csv('C:/Users/LuzHu/Desktop/表3.csv', index=False)

print("处理完成，结果已保存")
