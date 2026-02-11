library(ggplot2)
library(ggpubr)

# 加载数据
data <- read.csv("C:/Users/LuzHu/Desktop/B4c1b.csv", header = TRUE, row.names = 1)

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
  p <- ggplot(group_data, aes(x = .data[[x_var]], y = .data[[y_var]], colour = index, shape = index)) +
    geom_point() +
    geom_smooth(method = "lm", se = TRUE, fill = ci_color, color = ci_color) +
    scale_shape_manual(values = custom_shapes) +
    scale_colour_manual(values = custom_colors) +
    theme_bw() +
    theme(legend.position = "none", aspect.ratio = 1) +
    stat_cor(color= '#113A34', method = 'pearson', aes(x = .data[[x_var]], y = .data[[y_var]])) +
    xlab(paste(x_label, index_second_row, sep = " - ")) + ylab(y_label)
  
  return(p)
}

# 创建PDF文件
pdf("C:/Users/LuzHu/Desktop/output.pdf")

# 对每个组应用图表，针对Lat变量
plots_lat <- lapply(unique(data$index), function(group) {
  group_data <- subset(data, index == group)
  plot <- create_plot(group_data, "Fre", "Lat", "Frequency", "Latitude")
  print(plot)
})

# 对每个组应用图表，针对Long变量
plots_long <- lapply(unique(data$index), function(group) {
  group_data <- subset(data, index == group)
  plot <- create_plot(group_data, "Fre", "Long", "Frequency", "Longitude")
  print(plot)
})

dev.off()  # 关闭PDF设备
