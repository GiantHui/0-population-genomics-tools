# 安装并加载必要的包（如果没有安装）
if (!require("treestats")) install.packages("treestats")
if (!require("RSpectra")) install.packages("RSpectra")
if (!require("ape")) install.packages("ape")
if (!require("treestats")) install.packages("treestats")
# 加载包
library(treestats)
library(ape)
library(RSpectra)
library(treestats)
# 读取树文件
phylo_tree <- read.tree("C:/Users/victo/Desktop/Life.txt")

# 打印树的概述
print(phylo_tree)

# 计算所有统计量并打印结果
results <- calc_all_stats(phylo_tree)
print(results)


# 假设你只对某些物种或支系感兴趣，可以列出不需要的叶节点
tips_to_remove <- c("Tip1", "Tip2", "Tip3")  # 替换为你想删除的叶节点名称
# 使用 drop.tip 函数来剪枝
sub_tree <- drop.tip(phylo_tree, tips_to_remove)
# 打印子树概述
print(sub_tree)
# 计算子树的统计量
sub_tree_results <- calc_all_stats(sub_tree)
print(sub_tree_results)


# 假设你知道感兴趣支系的共同祖先节点ID
ancestor_node <- 50  # 这是假设的节点编号，替换为你感兴趣的支系节点ID
# 使用 extract.clade 提取从该节点开始的子树
sub_tree <- extract.clade(phylo_tree, ancestor_node)
# 打印子树概述
print(sub_tree)
# 计算子树的统计量
sub_tree_results <- calc_all_stats(sub_tree)
print(sub_tree_results)