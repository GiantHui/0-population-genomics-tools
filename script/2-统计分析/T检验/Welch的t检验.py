import pandas as pd
from scipy.stats import ttest_ind

# 读取数据
def read_data(file_path):
    return pd.read_csv(file_path)

# 执行Welch t检验
def perform_welch_t_test(data):
    group1 = data.iloc[:, 0].dropna()  # 第一列作为组1，并删除NaN值
    group2 = data.iloc[:, 1].dropna()  # 第二列作为组2，并删除NaN值
    t_stat, p_value = ttest_ind(group1, group2, equal_var=False)  # 使用equal_var=False进行Welch的t检验
    return t_stat, p_value

# 保存结果到文件
def save_results(file_path, t_stat, p_value):
    with open(file_path, 'w') as f:
        f.write("t-statistic: {}\n".format(t_stat))
        f.write("p-value: {}\n".format(p_value))
        if p_value < 0.05:
            f.write("两组Fst值之间存在显著差异。\n")
        else:
            f.write("两组Fst值之间不存在显著差异。\n")

# 主函数
def main():
    # 输入和输出数据文件路径
    input_file_path = "C:/Users/LuzHu/Desktop/1.csv"  # 修改为你的输入文件路径
    output_file_path = "C:/Users/LuzHu/Desktop/北南汉_北汉南少_t检验.txt"  # 修改为你的输出文件路径

    # 读取数据
    data = read_data(input_file_path)

    # 执行Welch t检验
    t_stat, p_value = perform_welch_t_test(data)

    # 输出结果到控制台
    print("t-statistic:", t_stat)
    print("p-value:", p_value)
    if p_value < 0.05:
        print("两组Fst值之间存在显著差异。")
    else:
        print("两组Fst值之间不存在显著差异。")

    # 保存结果到文件
    save_results(output_file_path, t_stat, p_value)

# 运行主函数
if __name__ == "__main__":
    main()
