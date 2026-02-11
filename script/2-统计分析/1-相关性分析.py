import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress
from aquarel import load_theme
# 使用pip install aquarel安装主题
# 配置主题
# sns.set_style("white")
theme = load_theme("boxy_light") # scientific,arctic_light,boxy_light,scientific,minimal_dark,minimal_light,arctic_dark
theme.apply()
# 配置字体
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# 读取数据文件
file_path = '/mnt/c/Users/Administrator/Desktop/Rice.csv'
output_fig_path = '/mnt/c/Users/Administrator/Desktop' 
data = pd.read_csv(file_path, sep=',')

# 定义颜色
scatter_color = '#81B3A8'
ci_color = '#A4C8C0'
ridge_color = '#A4C8E0'

# 动态获取index列的内容，用于标题
index_label = data['index'].iloc[0]
# 判断是否存在“Alt”列，创建相应数量的子图
if 'Alt' in data.columns:
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), gridspec_kw={'width_ratios': [5, 5, 5]})  # 3个子图
else:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [5, 5]})  # 2个子图

# 调整每个子图的边距和位置
plt.subplots_adjust(wspace=0.4)

# 定义嵌套函数用于添加紧靠子图边缘的山脊图
def add_ridge_plot(ax, x_data=None, frequency_data=None, color=ridge_color, orientation='vertical'):
    if orientation == 'horizontal':
        ridge_ax = ax.inset_axes([0, 1, 1, 0.15])  # 上方的山脊图
        sns.kdeplot(x=x_data, ax=ridge_ax, color=color, fill=True)
    else:
        ridge_ax = ax.inset_axes([1, 0, 0.15, 1])  # 右方的山脊图
        sns.histplot(frequency_data, ax=ridge_ax, bins=10, color=color, kde=True, element="step", fill=True)
    ridge_ax.axis('off')  # 隐藏坐标轴

# Latitude vs Frequency with 95% confidence interval
lat_slope, lat_intercept, lat_r_value, lat_p_value, lat_std_err = linregress(data['Lat'], data['Fre'])
sns.regplot(
    x='Lat', y='Fre', data=data, ax=axes[0], color=scatter_color, 
    line_kws={'color': scatter_color}, ci=95, scatter=False
)
axes[0].scatter(data['Lat'], data['Fre'], color=scatter_color, alpha=0.7, marker='^', s=50, label='Data Points')
axes[0].set_title(f'Latitude vs Frequency ({index_label})')
axes[0].set_xlabel('Latitude (Lat)')
axes[0].set_ylabel('Frequency (Fre)')
axes[0].legend([f'R = {lat_r_value:.2f}, p = {lat_p_value:.3f}'], loc='upper right')
add_ridge_plot(axes[0], x_data=data['Lat'], frequency_data=data['Fre'], color=ridge_color, orientation='horizontal')
# add_ridge_plot(axes[0], frequency_data=data['Fre'], color=ridge_color, orientation='vertical')

# Longitude vs Frequency with 95% confidence interval
long_slope, long_intercept, long_r_value, long_p_value, long_std_err = linregress(data['Long'], data['Fre'])
sns.regplot(
    x='Long', y='Fre', data=data, ax=axes[1], color=scatter_color, 
    line_kws={'color': scatter_color}, ci=95, scatter=False
)
axes[1].scatter(data['Long'], data['Fre'], color=scatter_color, alpha=0.7, marker='^', s=50, label='Data Points')
axes[1].set_title(f'Longitude vs Frequency ({index_label})')
axes[1].set_xlabel('Longitude (Long)')
axes[1].set_ylabel('Frequency (Fre)')
axes[1].legend([f'R = {long_r_value:.2f}, p = {long_p_value:.3f}'], loc='upper right')
add_ridge_plot(axes[1], x_data=data['Long'], frequency_data=data['Fre'], color=ridge_color, orientation='horizontal')
# add_ridge_plot(axes[1], frequency_data=data['Fre'], color=ridge_color, orientation='vertical')

# Altitude vs Frequency with 95% confidence interval (if Alt column exists)
if 'Alt' in data.columns:
    alt_slope, alt_intercept, alt_r_value, alt_p_value, alt_std_err = linregress(data['Alt'], data['Fre'])
    sns.regplot(
        x='Alt', y='Fre', data=data, ax=axes[2], color=scatter_color, 
        line_kws={'color': scatter_color}, ci=95, scatter=False
    )
    axes[2].scatter(data['Alt'], data['Fre'], color=scatter_color, alpha=0.7, marker='^', s=50, label='Data Points')
    axes[2].set_title(f'Altitude vs Frequency ({index_label})')
    axes[2].set_xlabel('Altitude (Alt)')
    axes[2].set_ylabel('Frequency (Fre)')
    axes[2].legend([f'R = {alt_r_value:.2f}, p = {alt_p_value:.3f}'], loc='upper right')
    add_ridge_plot(axes[2], x_data=data['Alt'], frequency_data=data['Fre'], color=ridge_color, orientation='horizontal')
    # add_ridge_plot(axes[2], frequency_data=data['Fre'], color=ridge_color, orientation='vertical')

# 保存并展示图表
plt.tight_layout()
theme.apply_transforms()
plt.savefig(f'{output_fig_path}/{index_label}.pdf')
plt.show()