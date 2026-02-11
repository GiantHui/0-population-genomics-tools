# 加载必要的R包
library(dplyr)  # 加载dplyr包，用于数据处理和管道操作
library(itol.toolkit)  # 加载itol.toolkit包，用于制作和管理iTOL树图的数据单元
library(data.table)  # 加载data.table包，提供高效的数据读取和操作功能
# # install.packages("pak")
# # 安装pkgbuild包
# pkgbuild::check_build_tools(debug = TRUE)

# install.packages("pkgbuild")
# # 检查并安装编译工具
# pkgbuild::check_build_tools(debug = TRUE)
# # from GitHub
# pak::pak('TongZhou2017/itol.toolkit')
# 设置工作目录
setwd("C:/Users/Administrator/Desktop")  # 将当前R会话的工作目录设置为指定路径

tree_1 <- "C:/Users/Administrator/Desktop/merged_dedup_biallelic.SNP.fasta.tree"  # 指定新克文件的路径，这个文件包含树的信息
hub_1 <- create_hub(tree_1)  # 创建一个以此树为中心的hub，用于添加不同的数据单元
data_file_1 <- "C:/Users/Administrator/Desktop/HP数据收集.csv"  # 指定元数据文件的路径
data_1 <- data.table::fread(data_file_1,header = TRUE)  # 使用data.table的fread函数读取元数据文件

#############################功能1################################################
# 为树的节点添加标签，按属分类
unit_1 <- create_unit(data = data_1 %>% select(ID, ML_NAME),  # 从data_1中选取ID和Genus列
                      key = "itol_3al_1_labels",  # 为这个单元设置一个键名
                      type = "LABELS",  # 设置数据单元的类型为标签
                      tree = tree_1)  # 指定这个单元关联的树文件
write_unit(unit_1, paste0(getwd(), "/Rename.txt"))  # 将单元写入文件

#############################功能2################################################
# 为树的分支添加颜色，按门分类
unit_2 <- create_unit(data = data_1 %>% select(ID, Classification_Chromopaniter_Detail),
                      key = "itol_3al_2_range",
                      type = "TREE_COLORS",  # 设置类型为树颜色
                      subtype = "branch",  # 子类型为范围，表示颜色将根据指定的范围变化
                      tree = tree_1)
write_unit(unit_2, paste0(getwd(), "/HAP.txt"))

#############################功能3################################################
# 为树添加颜色条带，按綱分类
set.seed(123)  # 设置随机数种子，确保颜色选择的可重复性
unit_3 <- create_unit(data = data_1 %>% select(ID, Chromopainter4),
                      key = "itol_3al_3_strip",
                      type = "DATASET_COLORSTRIP",  # 设置类型为颜色条带
                      color = "wesanderson",  # 使用Wes Anderson调色板
                      tree = tree_1)
unit_3@common_themes$basic_theme$margin <- 10  # 设置条带的边缘空白
write_unit(unit_3, paste0(getwd(), "/Chromopainter4_strip_Class.txt"))

#############################功能4################################################
# 添加柱状图，表示某个数值特征
unit_4 <- create_unit(data = data_1 %>% select(NAME,NUMBER_CHIP),
                      key = "itol_3al_4_simplebar",
                      type = "DATASET_SIMPLEBAR",  # 类型为简单柱状图
                      tree = tree_1)
unit_4@specific_themes$basic_plot$size_max <- 100  # 设置柱状图的最大宽度
write_unit(unit_4, paste0(getwd(), "/itol_3al_4_simplebar.txt"))

#############################功能5################################################
# 添加多数据柱状图，同时表示多个数值特
unit_5 <- create_unit(data = data_1 %>% select(NAME,NUMBER_CHIP,NUMBER_PUBLIC),
                      key = "itol_3al_5_multibar",
                      type = "DATASET_MULTIBAR",  # 类型为多数据柱状图
                      tree = tree_1)
unit_5@specific_themes$basic_plot$size_max <- 100  # 设置柱状图的最大宽度
write_unit(unit_5, paste0(getwd(), "/itol_3al_5_multibar.txt"))

#############################功能6################################################
# 添加梯度色柱状图，用于展示数据的变化
unit_6 <- create_unit(data = data_1 %>% select(ID, Elevation),
                      key = "itol_3al_6_gradient",
                      type = "DATASET_GRADIENT",  # 类型为渐变数据集
                      tree = tree_1)
unit_6@specific_themes$heatmap$color$min <- "#fac1c8"  # 设置渐变的最小颜色
unit_6@specific_themes$heatmap$color$mid <- "#cc5656"  # 设置渐变的中间颜色
unit_6@specific_themes$heatmap$color$max <- "#740808"  # 设置渐变的最大颜色
# 固定颜色映射的范围为 [0, 1]
unit_6@specific_themes$heatmap$min_value <- 0  # 最小值固定为 0
unit_6@specific_themes$heatmap$max_value <- 1  # 最大值固定为 1
write_unit(unit_6, paste0(getwd(), "/Elevation.txt"))

# 添加梯度色柱状图，用于展示数据的变化
unit_6 <- create_unit(data = data_1 %>% select(ID, Latitude),
                      key = "itol_3al_6_gradient",
                      type = "DATASET_GRADIENT",  # 类型为渐变数据集
                      tree = tree_1)
unit_6@specific_themes$heatmap$color$min <- "#b3f0e7"  # 设置渐变的最小颜色
unit_6@specific_themes$heatmap$color$mid <- "#26c3c6"  # 设置渐变的中间颜色
unit_6@specific_themes$heatmap$color$max <- "#083f38"  # 设置渐变的最大颜色
# 固定颜色映射的范围为 [0, 1]
unit_6@specific_themes$heatmap$min_value <- 0  # 最小值固定为 0
unit_6@specific_themes$heatmap$max_value <- 1  # 最大值固定为 1
write_unit(unit_6, paste0(getwd(), "/Latitude.txt"))

# 添加梯度色柱状图，用于展示数据的变化
unit_6 <- create_unit(data = data_1 %>% select(ID, Longitude),
                      key = "itol_3al_6_gradient",
                      type = "DATASET_GRADIENT",  # 类型为渐变数据集
                      tree = tree_1)
unit_6@specific_themes$heatmap$color$min <- "#c5e1f7"  # 设置渐变的最小颜色
unit_6@specific_themes$heatmap$color$mid <- "#65a9e5"  # 设置渐变的中间颜色
unit_6@specific_themes$heatmap$color$max <- "#041734"  # 设置渐变的最大颜色
# 固定颜色映射的范围为 [0, 1]
unit_6@specific_themes$heatmap$min_value <- 0  # 最小值固定为 0
unit_6@specific_themes$heatmap$max_value <- 1  # 最大值固定为 1
write_unit(unit_6, paste0(getwd(), "/Longitude.txt"))

#############################功能7################################################
# 绘制热图，用于展示多个变量的组合数据
unit_7 <- create_unit(data = data_1 %>% select(ID, NS, OS),
                      key = "itol_7_heatmap",
                      type = "DATASET_HEATMAP",  # 类型为热图
                      tree = tree_1)
write_unit(unit_7, paste0(getwd(), "/itol_7_heatmap.txt"))

#############################功能8################################################
# 生成每个唯一Class的随机颜色
class_unique <- unique(data_1$Class)  # 提取所有唯一的Class值
set.seed(123)  # 设置随机种子以保证颜色可以复现
colors <- sample(colors(), length(class_unique), replace = FALSE)  # 为每个Class随机分配颜色
class_colors <- setNames(colors, class_unique)  # 创建一个以Class为名称、颜色为值的向量
data_1$Color <- class_colors[data_1$Class]  # 将颜色值分配给相应的Class
unit_colors <- create_unit(data = select(data_1, ID, Color),
                           key = "itol_random_class_colors",
                           type = "TREE_COLORS",
                           subtype = "branch",  # 指定subtype为branch，可以改为range或clade
                           tree = tree_1)  # 请替换为您的树文件名称
write_unit(unit_colors, paste0(getwd(), "/itol_random_class_colors.txt"))
#############################功能9################################################
#############################功能9################################################
# 形状：1 矩形，2 圆形，3星形，4右边尖的三角形，5左边尖的三角形，6勾
unit_9 <- create_unit(data = data_1 %>%  select(ID, Host_species),
                      key = "Sample_Symbols", 
                      shape = 4,
                      type = "DATASET_SYMBOL",
                      position = 1,
                      size = 1,
                      subtype = "Symbol",
                      tree = tree_1,
                      fill = 1)
write_unit(unit_9,paste0(getwd(), "/Host_species.txt"))
