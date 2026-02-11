#使用ggcorrplot包绘制相关性热图

#首先安装ggcorrplot包
install.packages("ggcorrplot")
devtools::install_github("kassambara/ggcorrplot")


# 载入需要的package
library(ggcorrplot)

# 设置工作路径
setwd("D:/Y-chromosome/Affy/相关性分析")

# 加载或读取数据
gp <- read.csv("相关性.csv", header = TRUE, row.names = 1)  # 如果数据在CSV文件中
# 或者
#data(gp)# 如果数据已经内置在R中

#计算相关系数矩阵,这段代码将gp数据框中的所有变量两两之间的相关系数计算出来，并将结果四舍五入保留一位小数，保存在gpt变量中。如果gp是一个数据框，那么gpt将是一个包含了相关系数的矩阵。
gpt <- round(cor(gp), 1)# 计算相关系数矩阵并四舍五入到小数点后一位
#head(gpt[, 1:6])#查看第1-6列
#>       mpg  cyl disp   hp drat   wt
#> mpg   1.0 -0.9 -0.8 -0.8  0.7 -0.9
#> cyl  -0.9  1.0  0.9  0.8 -0.7  0.8
#> disp -0.8  0.9  1.0  0.8 -0.7  0.9
#> hp   -0.8  0.8  0.8  1.0 -0.4  0.7
#> drat  0.7 -0.7 -0.7 -0.4  1.0 -0.7
#> wt   -0.9  0.8  0.9  0.7 -0.7  1.0

#计算相关系数p值矩阵，这段代码使用cor_pmat函数计算了数据框gp中变量两两之间的相关系数的p值，并将结果保存在p.mat变量中。如果gp是一个数据框，那么p.mat将是一个包含了相关系数的p值的矩阵。
p.mat <- cor_pmat(gp)
#head(p.mat[, 1:4])#查看第1-4列
#>               mpg          cyl         disp           hp
#> mpg  0.000000e+00 6.112687e-10 9.380327e-10 1.787835e-07
#> cyl  6.112687e-10 0.000000e+00 1.802838e-12 3.477861e-09
#> disp 9.380327e-10 1.802838e-12 0.000000e+00 7.142679e-08
#> hp   1.787835e-07 3.477861e-09 7.142679e-08 0.000000e+00
#> drat 1.776240e-05 8.244636e-06 5.282022e-06 9.988772e-03
#> wt   1.293959e-10 1.217567e-07 1.222320e-11 4.145827e-05

# 创建并打开一个PDF文件
pdf("correlation_ggcorrplot2.pdf", width=11, height=8.5)


#首先进行一个简单绘制，默认为方形
ggcorrplot(gpt, tl.cex = 8)
#将样式改为圆形，method="circle"
ggcorrplot(gpt, tl.cex = 8, method = "circle")
#使用hc.order关键字做层次聚类（hierarchical clustering）
ggcorrplot(gpt, tl.cex = 8, hc.order = TRUE, outline.color = "white")
#通过type=="lower"关键字来做下三角效果：
ggcorrplot(gpt, tl.cex = 8,
                hc.order = TRUE,
                type = "lower",
                outline.color = "white")
#同理利用type = "upper"关键字做上三角效果：
ggcorrplot(gpt, tl.cex = 8,
           hc.order = TRUE,
           type = "upper",
           outline.color = "white",
           ggtheme = ggplot2::theme_gray,
           colors = c("#6D9EC1", "white", "#E46726"))
#还可以标注显著性，通过lab = TRUE关键字:
ggcorrplot(gpt, tl.cex = 8,
           hc.order = TRUE,
           type = "lower",
           lab = TRUE,  lab_size = 2)
#通过关键字手动根据p值标注显著性，不显著的地方画叉号：
ggcorrplot(gpt, tl.cex = 8,
           hc.order = TRUE,
           type = "lower",
           p.mat = p.mat,
           sig.level = c(0.05, 0.01, 0.001), # 可以指定显著性水平
           insig = "blank", # 不显著时显示为空白
           outline.color = "white") # 边框颜色为白色

ggcorrplot(gpt, tl.cex = 8,
           hc.order = TRUE,
           type = "lower",
           p.mat = p.mat,
           sig.level = c(0.05, 0.01, 0.001), # 可以指定显著性水平
           insig = "pch",
           pch = 4,#用于表示不显著相关系数的符号代码(是"x形")
           pch.col = "black",
           pch.cex = 2,# 用于表示不显著相关系数的符号代码大小
           outline.color = "white") # 边框颜色为白色


# 结束，PDF输出
dev.off()



---------------------------------------------------------------------------------------------------
ggcorrplot(
  corr,
  method = c("square", "circle"),
  type = c("full", "lower", "upper"),
  ggtheme = ggplot2::theme_minimal,
  title = "",
  show.legend = TRUE,
  legend.title = "Corr",
  show.diag = NULL,
  colors = c("blue", "white", "red"),
  outline.color = "gray",
  hc.order = FALSE,
  hc.method = "complete",
  lab = FALSE,
  lab_col = "black",
  lab_size = 4,
  p.mat = NULL,
  sig.level = 0.05,
  insig = c("pch", "blank"),
  pch = 4,
  pch.col = "black",
  pch.cex = 5,
  tl.cex = 12,
  tl.col = "black",
  tl.srt = 45,
  digits = 2,
  as.is = FALSE
)

cor_pmat(x, ...)

这里是ggcorrplot函数的参数含义：

corr: 要绘制的相关系数矩阵。
method: 相关系数的绘制方法，可以是"square"（正方形）或"circle"（圆形）。
type: 要显示的相关系数的类型，可以是"full"（全部显示）、"lower"（只显示下三角部分）、"upper"（只显示上三角部分）。
ggtheme: 使用的ggplot2主题。
title: 图表的标题。
show.legend: 是否显示图例。
legend.title: 图例标题。
show.diag: 是否显示对角线元素。
colors: 相关系数的颜色范围。
outline.color: 边框颜色。
hc.order: 是否对相关系数进行层次聚类并按照聚类结果重新排序。
hc.method: 层次聚类方法。
lab: 是否显示标签。
lab_col: 标签颜色。
lab_size: 标签大小。
p.mat: 显著性矩阵。
sig.level: 显著性水平。
insig: 用于表示不显著的相关系数的符号或留白。
pch: 用于表示不显著的相关系数的点的形状。
pch.col: 不显著的相关系数的点的颜色。
pch.cex: 不显著的相关系数的点的大小。
tl.cex: 标题和标签的大小。
tl.col: 标题和标签的颜色。
tl.srt: 标题和标签的旋转角度。
digits: 相关系数的小数位数。
as.is: 是否保持相关系数的原始值。
此外，还有一个cor_pmat函数，用于计算相关系数的显著性水平，其参数与ggcorrplot中的参数共享。
---------------------------------------------------------------------------------------------------------------
corr: 要可视化的相关系数矩阵。
method: 相关系数矩阵的可视化方法，可以是"square"（正方形）或"circle"（圆形）。
type: 要显示的相关系数的类型，可以是"full"（全部显示）、"lower"（只显示下三角部分）或"upper"（只显示上三角部分）。
ggtheme: 使用的ggplot2主题。
title: 图表的标题。
show.legend: 是否显示图例。
legend.title: 图例标题。
show.diag: 是否显示主对角线上的相关系数。
colors: 用于表示低、中、高相关系数的颜色向量。
outline.color: 方块或圆形的边框颜色。
hc.order: 是否对相关系数进行层次聚类并重新排序。
hc.method: 层次聚类方法。
lab: 是否在图中显示相关系数。
lab_col、lab_size：相关系数标签的颜色和大小（当lab = TRUE时使用）。
p.mat: 相关系数的p值矩阵。如果为NULL，则忽略sig.level、insig、pch、pch.col和pch.cex参数。
sig.level: 显著性水平，如果p值大于此值，则相关系数被视为不显著。
insig: 用于表示不显著相关系数的方式，可以是"pch"（添加特定符号）或"blank"（留白）。
pch: 用于表示不显著相关系数的符号代码（仅在insig = "pch"时有效）。
pch.col、pch.cex：不显著相关系数符号的颜色和大小（仅在insig = "pch"时有效）。
tl.cex、tl.col、tl.srt：文本标签（变量名称）的大小、颜色和旋转角度。
digits: 相关系数的小数位数。
as.is: 传递给melt.array的逻辑值。如果为TRUE，则dimnames将保留为字符串而不转换为数值。
x: 数值矩阵或数据框，包含要计算相关系数的数据。
...: 其他要传递给cor.test函数的参数。


ggcorrplot函数返回一个ggplot2对象，而cor_pmat函数返回一个包含相关系数的p值的矩阵。

pch参数用于指定在图中表示不显著相关系数的点的符号代码。在R中，pch参数可以使用以下符号代码：
0：方块
1：空心圆
2：空心三角形
3：十字
4：X形
5：空心菱形
6：空心倒三角形
7：方块加X形
8：星形
9：菱形加十字
10：空心圆加十字
11：六角星形
12：田字形

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 载入需要的package
library(ggcorrplot)

# 设置工作路径
setwd("D:/Y-chromosome/Affy/相关性分析")

# 加载或读取数据
gp <- read.csv("相关性.csv", header = TRUE, row.names = 1)

#计算相关系数矩阵,这段代码将gp数据框中的所有变量两两之间的相关系数计算出来，并将结果四舍五入保留一位小数，保存在gpt变量中。如果gp是一个数据框，那么gpt将是一个包含了相关系数的矩阵。
gpt <- round(cor(gp), 1)# 计算相关系数矩阵并四舍五入到小数点后一位

#计算相关系数p值矩阵，这段代码使用cor_pmat函数计算了数据框gp中变量两两之间的相关系数的p值，并将结果保存在p.mat变量中。如果gp是一个数据框，那么p.mat将是一个包含了相关系数的p值的矩阵。
p.mat <- cor_pmat(gp)

# 创建并打开一个PDF文件
pdf("test2.pdf", width=11, height=8.5)

#首先进行一个简单绘制，默认为方形
ggcorrplot(gpt, tl.cex = 8)+
                                     geom_tile(width = 0.25, height = 0.25)  # 调整方块的大小为0.25
#将样式改为圆形，method="circle"
ggcorrplot(gpt, tl.cex = 8, method = "circle")+
                                     geom_tile(width = 0.25, height = 0.25)  # 调整圆形的大小为0.25

ggcorrplot(gpt, tl.cex = 8)+
                                     geom_tile(width = 0.5, height = 0.5)  # 调整方块的大小为0.5
#将样式改为圆形，method="circle"
ggcorrplot(gpt, tl.cex = 8, method = "circle")+
                                     geom_tile(width = 0.5, height = 0.25)  # 调整圆形的大小为0.5

ggcorrplot(gpt, tl.cex = 8)+
                                     geom_tile(width = 0.8, height = 0.8)  # 调整方块的大小为0.8
#将样式改为圆形，method="circle"
ggcorrplot(gpt, tl.cex = 8, method = "circle")+
                                     geom_tile(width = 0.8, height = 0.8)  # 调整圆形的大小为0.8

# 结束，PDF输出
dev.off()