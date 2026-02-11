library(ggtree)
library(treeio)
library(tidyverse)
library(ggtreeExtra)
library(ggnewscale)
library(ggsci)
# 设置工作目录
setwd("/mnt/d/幽门螺旋杆菌/Script/分析结果/5-ggtree")
# 加载系统发生树文件(WGS)
WGS_tree <- read.tree("./data/东亚高地和低地_VeryFastTree.rooted_normal_branch.tree")

##* 分支着色
# 文件路径可按需修改
group_file <- "./conf/group.txt" #todo 第一列是label(ID)，第二列是group(单倍群)，不包含表头
color_file <- "./conf/color.txt" #todo 第一列是group(单倍群)，第二列是color，不包含表头

# 读取分组信息
group_df <- read.table(group_file, header = FALSE, sep = "\t", stringsAsFactors = FALSE, col.names = c("label", "group"))
group_list <- split(group_df$label, group_df$group) # 将分组信息转换为列表

# 读取颜色信息
color_df <- read.table(color_file, header = FALSE, sep = "\t", stringsAsFactors = FALSE, comment.char = '', col.names = c("group", "color"))
group_colors <- setNames(color_df$color, color_df$group) # 将颜色信息转换为命名向量

# 读取树并分组
tree_grouped <- groupOTU(WGS_tree, group_list)


#* 计算从节点到叶子的距离（树的高度 - 节点深度）
#? BEAST等软件不需要计算，自带
node_heights <- node.depth.edgelength(WGS_tree)
max_height <- max(node_heights)
node_to_tip_distance <- max_height - node_heights

#*===================================================================================
#* 使用ggtree绘制系统发育树
p0 <-ggtree(tree_grouped, aes(color = group), layout = 'rectangular',open.angle = 5, lwd = 0.2) +
  scale_color_manual(values = group_colors) +
  geom_tiplab(size = 0.5, align = TRUE,hjust = -0.5) + #* 添加tiplab，默认显示`label`
  geom_nodepoint(size=0.3) +   #* 添加nodepoint
  geom_nodelab(aes(label=round(branch.length, 3)), hjust=-0.3, size=0.7) + #* 显示branch.length
  geom_nodelab(aes(label=round(node_to_tip_distance[node], 3)), hjust=1, color="#000000", size=0.7) + #*显示树的高度（到叶子节点的距离）
  theme_tree2() + # 显示坐标轴
  theme(
    axis.text.x = element_text(size = 2),    # x轴刻度文字大小
    axis.title.x = element_text(size = 2),    # x轴标题文字大小
    axis.text.y = element_text(size = 2),    # y轴刻度文字大小
    axis.title.y = element_text(size = 2)     # y轴标题文字大小
  ) +
  scale_x_continuous(
    expand = expansion(mult = c(0.02, 0.03)),
    breaks = seq(0, max(node_heights), by = 5000), #* 每5000年一个刻度，自行修改以对应不同的时间树
    labels = function(x) format(round(x), big.mark=","), #* 添加千位分隔符
    name = "Time (years ago)"
  ) + #* 扩展x轴空间，左边2%，右边3%
  scale_y_continuous(expand = expansion(mult = c(0.01, 0.01))) + #* 扩展y轴空间，上下各1%
  geom_vline(xintercept = seq(0, max(node_heights), by = 5000), 
             color = "#1c9cc6", linetype = "solid", alpha = 0.3, linewidth = 0.05) + # 每5000年一条细红线
  geom_vline(xintercept = seq(0, max(node_heights), by = 10000), 
             color = "#196c88", linetype = "solid", alpha = 0.5, linewidth = 0.1)   # 每10000年一条粗蓝线

ggsave(p0, filename = '../output/系统发育树.pdf', units = "cm", height = 20 ,width = 15 )
#*===================================================================================

##* 使用ggtreeExtra美化
# 首先读取meta信息文件
meta_file <- "./conf/HP数据收集2.xlsx"
df_META <- readxl::read_excel(meta_file, sheet = 'HP数据收集')
tree_grouped |> as.treedata() -> tree_grouped_S4
# 将df_META和tree_grouped_S4结合
full_join(tree_grouped_S4, df_META, by = c("label" = "ID")) -> tree_grouped_S4_META
# 将高海拔菌株和低海拔菌株的MRCA旋转一下更美观
# #* 采用flip方法交换2个节点的位置。
# #* 首先找到高低的MRCA节点
# tree_grouped_S4 |> MRCA("HEL_CA3369AA_AS","HEL_CA2296AA_AS") -> MRCA_node
# tree_grouped_S4 |> child(MRCA_node) # 输出结果是7594 9269
# #! 旋转之前一定加上ggtree::flip()，不然会和ape包的flip()函数冲突
# ggtree::flip(p0,7594,9269) -> p1

# 挑选df_META中Province为空的行，将其的Country内容填充到Province列
n_provinces <- length(unique(df_META$Province))
# 使用colorRampPalette生成足够的颜色
province_colors <- colorRampPalette(RColorBrewer::brewer.pal(12, "Set3"))(n_provinces)


p2 <- p0 +  
new_scale_fill() +
    geom_fruit(
    data = filter(df_META,Species != 'H. pylori'),
    geom = geom_point,
    mapping = aes(y = ID ,color =Species, shape = Species),
    size = 1,
    position = "identity" #!重要参数，保证了位置恰好在树的分支末端
    ) +  
new_scale_fill() +
    geom_fruit(
    data = filter(df_META,Ecotype != 'Ubiquitous'),
    geom = geom_point,
    mapping = aes(y = ID ,color =Ecotype, shape = Ecotype),
    size = 1,
    position = "identity" #!重要参数，保证了位置恰好在树的分支末端
    ) +  
new_scale_fill() +
    geom_fruit(
    data = filter(df_META),
    geom = geom_tile,
    mapping = aes(y = ID ,fill = Province),
    width = 0.01,
    offset = -0.02
    ) + scale_fill_manual(values = province_colors) +
new_scale_fill() +
    geom_fruit(
    data = filter(df_META),
    geom = geom_tile,
    mapping = aes(y = ID ,fill =Elevation),
    width = 0.01,
    offset = 0.03
    )+ scale_fill_gradient(low = "#FAC1C8", high = "#740808") 
new_scale_fill() +
    geom_fruit(
    data = filter(df_META),
    geom = geom_tile,
    mapping = aes(y = ID ,fill =Latitude),
    width = 0.01,
    offset = 0.03
    )+  scale_fill_gradient(low = "#B3F0E7", high = "#083F38") +
new_scale_fill() +
    geom_fruit(
    data = filter(df_META),
    geom = geom_tile,
    mapping = aes(y = ID ,fill =Longitude),
    width = 0.01,
    offset = 0.03
    ) + scale_fill_gradient(low = "#C5E1F7", high = "#041734") 
ggsave(p2,filename = './output/东亚高地和低地_VeryFastTree.rooted_normal_branch.fan.pdf',height = 10,width = 15)

