# ================================
# 共祖节点时间统计与可视化脚本（合并图）
# ================================

library(ape)
library(ggplot2)
library(dplyr)
library(tibble)

# ========= 参数配置 =========
setwd("C:/Users/LuzHu/Desktop/") # 设置工作目录
tree_file <- "Nanjing_38.final.trees"
output_csv <- "Nanjing_38_node_times.csv"
bin_resolution <- 1000
time_range <- c(50000, 0)
# ============================

# Step 1: 读取树
if (!file.exists(tree_file)) stop("❌ 树文件不存在，请检查路径。")
tree <- read.nexus(tree_file)

# Step 2: 节点高度与分化时间
node_heights <- node.depth.edgelength(tree)
max_height <- max(node_heights)
divergence_times <- max_height - node_heights

# Step 3: 内部节点时间
n_tips <- length(tree$tip.label)
internal_nodes <- (n_tips + 1):(n_tips + tree$Nnode)
internal_node_times <- divergence_times[internal_nodes]

# Step 4: 分箱统计
node_df <- tibble(
  Divergence_Time = round(internal_node_times / bin_resolution) * bin_resolution
)

summary_df <- node_df %>%
  count(Divergence_Time, name = "New_Nodes") %>%
  arrange(desc(Divergence_Time)) %>%
  mutate(Cumulative_Nodes = cumsum(New_Nodes)) %>%
  arrange(Divergence_Time)

# Step 5: 输出CSV
write.csv(summary_df, output_csv, row.names = FALSE)
cat("✅ 共祖节点时间统计已保存至：", output_csv, "\n")

# Step 6: 合并图：柱状图 + 折线图（双Y轴）
scale_factor <- max(summary_df$New_Nodes) / max(summary_df$Cumulative_Nodes)

p_combined <- ggplot(summary_df, aes(x = Divergence_Time)) +
  geom_col(aes(y = New_Nodes), fill = "steelblue", width = bin_resolution * 0.9) +
  geom_line(aes(y = Cumulative_Nodes * scale_factor), color = "darkblue", size = 1.2) +
  scale_x_reverse(limits = time_range, expand = c(0, 0)) +
  scale_y_continuous(
    name = "新增节点数",
    sec.axis = sec_axis(~ . / scale_factor, name = "累计节点数")
  ) +
  labs(title = "共祖节点数统计（新增 vs 累计）", x = "分化时间（年 BP）") +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(size = 15, face = "bold"),
    axis.title.y.left = element_text(color = "steelblue"),
    axis.title.y.right = element_text(color = "darkblue")
  )

# Step 7: 绘图
print(p_combined)
