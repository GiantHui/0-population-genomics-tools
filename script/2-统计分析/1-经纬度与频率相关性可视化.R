library(tidyverse)
library(patchwork)
library(ggpubr)
library(ggExtra)
#! 使用之前按照`6-经纬度-频率-线性相关/markdown/0-使用说明.md`准备文件
# 设置工作目录
setwd('/mnt/f/OneDrive/文档（科研）/脚本/Download/5-Geographic/6-经纬度-频率-线性相关')
# 加载数据
data <- read.csv('./conf/1.csv', header = TRUE, row.names = 1)
data
# 检查数据是否包含NULL值或其他异常情况
if (any(is.null(data)) || any(is.na(data))) {
  stop("数据中包含NULL或NA值，请检查数据文件。")
}

# 获取所有unique的index值
unique_indices <- unique(data$index)

#TODO 自定义形状和颜色
scatter_shapes <- c(17)  # 设置点的形状为三角形
scatter_size <- 2.5  # 设置散点的大小
line_width <- 1.5  # 设置线条宽度
custom_colors <- c("#81B3A9")  # 设置点的颜色
ci_color <- "#C1DDDB"  # 置信区间的颜色

# 定义一个函数，用于创建图表
create_plot <- function(group_data, x_var, y_var, x_label, y_label, index_name) {
  # 计算相关系数和p值
  cor_test <- cor.test(group_data[[x_var]], group_data[[y_var]], method = "pearson")
  r_value <- round(cor_test$estimate, 3)
  p_value <- cor_test$p.value
  
  # 格式化p值
  if (p_value < 0.001) {
    p_text <- "p < 0.001"
  } else {
    p_text <- paste("p =", round(p_value, 3))
  }
  
  # 创建连续的标签文本
  cor_label <- paste("R =", r_value, "", p_text)
  
  # 创建基础散点图
  p <- ggplot(group_data, aes(x = .data[[x_var]], y = .data[[y_var]])) +
    geom_point(size = scatter_size, color = custom_colors, shape = scatter_shapes) +
    geom_smooth(method = "lm", se = TRUE, fill = ci_color, color = ci_color, size = line_width) +
    theme_bw() +
    theme(
        panel.grid.major = element_line(color = alpha("#bdfdf4", 0.5)),
        panel.grid.minor = element_line(color = alpha("#dffffe", 0.3)),
        aspect.ratio = 1
        ) +
    annotate("text", 
             x = -Inf, y = Inf, 
             label = cor_label,
             hjust = -0.1, vjust = 1.1,
             color = '#113A34',
             size = 3.5) +
    xlab(paste(x_label, index_name, sep = ": ")) + ylab(y_label)
  
  # 添加边缘密度图
  p_with_marginals <- ggMarginal(
    p, 
    type = "density",
    margins = "both",
    size = 10,
    fill = "#81B3A9",
    color = "#81B3A9",
    alpha = 0.7
  )
  
  return(p_with_marginals)
}

# 为每个unique的index创建图形
all_plots <- list()

for (index_value in unique_indices) {
  # 筛选当前index的数据
  group_data <- subset(data, index == index_value)
  
  # 创建纬度图
  plot_lat <- create_plot(group_data, "Fre", "Lat", "Frequency", "Latitude", index_value)
  
  # 创建经度图
  plot_long <- create_plot(group_data, "Fre", "Long", "Frequency", "Longitude", index_value)
  
  # 将两个图添加到列表中
  all_plots <- append(all_plots, list(plot_lat, plot_long))
}

# 使用patchwork组合所有图形，每行2个图（纬度和经度）
combined_plot <- wrap_plots(all_plots, ncol = 2) + 
  plot_annotation(tag_levels = 'A') &  # 添加A, B, C, D...标签
  theme(plot.tag = element_text(size = 12, face = "bold"))  # 设置标签样式

# 保存组合后的图形
ggsave(
  "./output/combined_plots.pdf",
  plot = combined_plot,
  width = 12,
  height = 6 * length(unique_indices),  # 根据index数量调整高度
  units = "in"
)
