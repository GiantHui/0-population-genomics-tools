#install.packages("ggpubr")
library(ggplot2)  # 加载ggplot2库，用于数据可视化
library(ggpubr)  # 加载ggpubr库，用于增强的ggplot2图表
# library(ggExtra)  # 注释掉ggExtra库的加载，因为不再使用边际图

# 加载数据
data <- read.csv("C:/Users/victo/Desktop/新建_Text_Document_Altitude_Western Siberian nomadic populations.txt",sep = "\t", header = TRUE, row.names = 1)

# 检查数据是否包含NULL值或其他异常情况
if (any(is.null(data)) || any(is.na(data))) {
  stop("数据中包含NULL或NA值，请检查数据文件。")
}

# 获取index列的第二行的值
index_second_row <- data$index[2]

# 自定义形状和颜色
custom_shapes <- c(17)  # 设置点的形状为三角形
custom_colors <- c("#81B3A9")  # 设置点的颜色
ci_color <- "#C1DDDB"  # 置信区间的颜色

# 定义一个函数，用于创建图表
create_plot <- function(group_data, x_var, y_var, x_label, y_label) {
  # 创建基础散点图，添加线性拟合线和相关系数
  p <- ggplot(group_data, aes(x = .data[[x_var]], y = .data[[y_var]], colour = index, shape = index)) +
    geom_point() +  # 添加散点
    geom_smooth(method = "lm", se = TRUE, fill = ci_color, color = ci_color) +  # 添加线性拟合线，显示95%置信区间，置信区间颜色为ci_color
    scale_shape_manual(values = custom_shapes) +  # 应用自定义点形状
    scale_colour_manual(values = custom_colors) +  # 应用自定义点颜色
    theme_bw() +  # 使用白色背景主题
    theme(legend.position = "none",  # 隐藏图例
          aspect.ratio = 1) +  # 设置图表为正方形
    stat_cor(color= '#113A34',method = 'pearson', aes(x = .data[[x_var]], y = .data[[y_var]])) +  # 计算并显示Pearson相关系数
    xlab(paste(x_label, index_second_row, sep = " - ")) + ylab(y_label)  # 设置坐标轴标签
  
  return(p)
}

# # 对每个组应用图表，针对Lat变量
# plots_lat <- lapply(unique(data$index), function(group) {
#   group_data <- subset(data, index == group)  # 按组过滤数据
#   create_plot(group_data, "Fre", "Lat", "Fre", "Lat")  # 创建并返回图表
# })

# # 对每个组应用图表，针对Long变量
# plots_long <- lapply(unique(data$index), function(group) {
#   group_data <- subset(data, index == group)  # 按组过滤数据
#   create_plot(group_data, "Fre", "Long", "Fre", "Long")  # 创建并返回图表
# })

# # 在网格布局中显示所有图表
# final_plot <- ggarrange(plotlist = c(plots_lat, plots_long), ncol = 2, nrow = ceiling((length(plots_lat) + length(plots_long)) / 2))  # 使用2列布局，行数根据图表总数动态计算
# print(final_plot)


##########单独对海拔进行绘图
# 对每个组应用图表，针对Alt变量
plots_Alt <- lapply(unique(data$index), function(group) {
  group_data <- subset(data, index == group)  # 按组过滤数据
  create_plot(group_data, "Fre", "Alt", "Fre", "Alt")  # 创建并返回图表
})
# 在网格布局中显示所有图表
final_plot <- plots_Alt
print(final_plot)
