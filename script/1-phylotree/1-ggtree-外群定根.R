# # 加载必要的库
# library(tidyverse)
# library(ggtree)
# library(treeio)
# library(ape)

# # 设置工作目录
# setwd("/mnt/d/幽门螺旋杆菌/Script/分析结果/5-ggtree")
# Input_tree <- './data/东亚高地和低地_VeryFastTree.tree'
# Output_tree <- './data/东亚高地和低地_VeryFastTree.rooted.tree'
# # 1. 数据加载步骤
# # 加载系统发生树文件(WGS)
# WGS_tree <- read.tree(Input_tree)

# # 加载元数据
# df_META <- readxl::read_excel("./conf/HP数据收集2.xlsx", sheet = 'HP数据收集')
# df_sim_META <- df_META |>
#    select(ID, `7544个样本`, Chromopainter4, Latitude, Longitude, 
#           Elevation, Continent, Country, Species, Ecotype)

# # 2. 树注释步骤
# # 将元数据与树关联
# GWS_tree_META <- WGS_tree |>
#    left_join(df_sim_META, by = c("label" = "ID"))

# # 确定用于根化的外群
# outgroup_samples <- GWS_tree_META |> as_tibble() |>
#    filter((Chromopainter4 == "hpAfrica2") & (Species != 'H. pylori'))

# # 提取外群样本的节点ID
# outgroup_nodes <- outgroup_samples |>
#    select(node) |>
#    pull()

# # 找到外群的最近共同祖先节点(MRCA)用于根化
# MRCA_node <- GWS_tree_META |> MRCA(outgroup_nodes)

# # 3. 树的根化步骤
# # 使用MRCA节点对树进行根化
# # 注意：由于treeio的bug，先转换为phylo对象，然后进行根化，再转换回来
# rooted_phylo <- GWS_tree_META |> 
#    as.phylo() |> 
#    root.phylo(node = MRCA_node, resolve.root = TRUE, edgelabel = TRUE)

# # 4. 将根化后的树导出为新的Newick文件
# # 导出为Newick格式
# write.tree(rooted_phylo, file = Output_tree)

# # 打印确认信息
# cat("根化后的树已导出\n")


# 加载必要的包
library(ape)

# 读取树文件
tree <- read.tree("1.nwk")

# 将树重新定根到 label 为 "RSRS" 的节点
tree_rooted <- root(tree, outgroup = "RSRS", resolve.root = TRUE)

# 导出新的 rooted 树
write.tree(tree_rooted, file = "1_rooted.nwk")
