from pathlib import Path
from typing import Sequence, Union, Tuple, List
import argparse
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# --- 全局配置 ---
FIGURE_SIZE = (7, 3.5)
FONT_CONFIG = {
    "font.family": "Arial",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}
PLOT_CONFIG = {
    "bar_label_fontsize": 6,
    "pie_label_fontsize": 6,
    "pie_start_angle": 140,
    "pie_label_distance": 1.1,
}
CUSTOM_COLORS = [
    "#D55E00", "#E39400", "#E0C318","#7AB241", 
    "#7AB241","#009E73","#2AA9AD","#56B4E9",
    "#40AECB","#238DC8", "#2B93CD", "#0072B2" ,
]

# 应用全局配置
plt.rcParams.update(FONT_CONFIG)

def create_color_gradient(n: int, colors: Sequence[str] = CUSTOM_COLORS) -> Sequence[Tuple[float, float, float, float]]:
    """创建渐变色方案"""
    cmap = LinearSegmentedColormap.from_list("custom_gradient", colors, N=n)
    return cmap(range(n))

def collapse_low_frequency_categories(
    value_counts: pd.Series,
    top_n: int = 30,
    other_category: str = "Other"
) -> pd.Series:
    """将低频类别合并为"其他"类别"""
    if len(value_counts) <= top_n:
        return value_counts
        
    top_categories = value_counts.iloc[:top_n]
    other_sum = value_counts.iloc[top_n:].sum()
    return pd.concat([top_categories, pd.Series({other_category: other_sum})])

def create_subplot(
    ax_bar: plt.Axes,
    ax_pie: plt.Axes,
    counts: pd.Series,
    title: str
) -> None:
    """创建单个子图组（柱状图和饼图）"""
    if counts.empty:
        return

    colors = create_color_gradient(len(counts))
    
    # 柱状图
    bars = ax_bar.bar(counts.index, counts.values, color=colors)
    ax_bar.set_ylabel("Number")
    ax_bar.tick_params(axis="x", rotation=90)
    # 设置柱状图数据标签颜色与柱子颜色一致
    for i, (bar, color) in enumerate(zip(bars, colors)):
        height = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom',
                    fontsize=PLOT_CONFIG["bar_label_fontsize"],
                    color=color)
    ax_bar.grid(False)
    ax_bar.set_title(f"{title} - Bar Plot")

    # 饼图
    total = counts.sum()
    labels = [f"{k} ({v/total:.1%})" for k, v in counts.items()]
    # 设置饼图文本颜色与扇形颜色一致
    wedges, texts = ax_pie.pie(
        counts.values,
        labels=labels,
        colors=colors,
        startangle=PLOT_CONFIG["pie_start_angle"],
        labeldistance=PLOT_CONFIG["pie_label_distance"],
        textprops={"fontsize": PLOT_CONFIG["pie_label_fontsize"]},
    )
    # 更新饼图标签颜色
    for text, color in zip(texts, colors):
        text.set_color(color)
    ax_pie.set_title(f"{title} - Pie Chart")

def create_visualization(
    df: pd.DataFrame,
    cols: List[str],
    top_n: int,
    output_path: Path
) -> None:
    """创建多列的组合可视化"""
    n_cols = len(cols)
    fig = plt.figure(figsize=(FIGURE_SIZE[0], FIGURE_SIZE[1] * n_cols))
    
    for idx, col in enumerate(cols, 1):
        # 计算频率
        value_counts = df[col].dropna().astype(str).value_counts()
        value_counts = collapse_low_frequency_categories(value_counts, top_n)
        
        # 导出统计结果到txt
        txt_path = output_path.parent / f"{col}_分类数量.txt"
        value_counts.to_csv(txt_path, sep="\t", header=["Number"])
        
        # 创建子图
        ax_bar = plt.subplot(n_cols, 2, 2*idx-1)
        ax_pie = plt.subplot(n_cols, 2, 2*idx)
        create_subplot(ax_bar, ax_pie, value_counts, col)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="生成类别统计的柱状图和饼图")
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="输入文件路径（支持.csv, .xlsx, .txt等格式）"
    )
    parser.add_argument(
        "-s", "--sep",
        type=str,
        default="\t",
        help="输入文件的分隔符（默认为制表符\\t）"
    )
    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=30,
        help="每个类别保留的top项数量（默认为30）"
    )
    parser.add_argument(
        "-c", "--columns",
        type=str,
        required=True,
        help="需要绘制的列名，多个列名用逗号分隔"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="输出文件目录路径（默认为当前目录）"
    )
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_args()
    
    # 处理输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在：{input_path}")
    
    # 根据文件后缀选择读取方法
    suffix = input_path.suffix.lower()
    if suffix == '.csv' or suffix == '.txt':
        df = pd.read_csv(input_path, sep=args.sep)
    elif suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path)
    else:
        raise ValueError(f"不支持的文件格式：{suffix}")
    
    # 处理列名
    columns = [col.strip() for col in args.columns.split(",")]
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"以下列在输入文件中不存在：{', '.join(missing_cols)}")
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建可视化
    print(f"目前使用的颜色列表为: {CUSTOM_COLORS};") 
    print(f"如需要修改图标大小，字体系列等，请在python脚本顶部修改") 
    output_path = output_dir / f"分类统计_{'-'.join(columns)}.pdf"
    create_visualization(df, columns, args.top_n, output_path)
    print(f"统计结果已保存到：{output_dir}")

if __name__ == "__main__":
    main()