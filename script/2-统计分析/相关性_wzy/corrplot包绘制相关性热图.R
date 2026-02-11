#使用corrplot包绘制相关性热图

# 在开始之前请确保你已经安装了下列package
install.packages("corrplot")


# 设置工作路径
setwd("D:/Y-chromosome/Affy/相关性分析")

# 载入需要的package
library(corrplot)

# 读取数据
gp <- read.csv("相关性.csv", header = TRUE, row.names = 1)

# 将所有非数值型的列转换为数值型
#gp[] <- lapply(gp, as.numeric)

# 计算相关系数矩阵
gpt <- cor(gp, method = "pearson", use = "pairwise.complete.obs")


# 创建并打开一个PDF文件
pdf("correlation_plot1.pdf", width=11, height=8.5)

# 绘制相关性图1 - circle，调标题颜色tl.col = "black",大小 tl.cex = 1.2,角度 tl.srt = 45
corrplot(gpt, method = "circle", 
         tl.col = "black", tl.cex = 0.8, tl.srt = 45)

# 绘制相关性图2 - number
corrplot(gpt, method = "number",
         tl.col = "black", tl.cex = 0.8, tl.srt = 45, number.cex = 0.3)


# 更改参数，只留一半
corrplot(gpt, method = "number",
         type = "upper",
         tl.col = "black", tl.cex = 0.8, tl.srt = 45, number.cex = 0.3)


# 组合式，左下展示相关系数，右上展示ellipse图形
corrplot(gpt, method = "ellipse", type = "upper",
         tl.col = "black", tl.cex = 0.8, tl.srt = 45, tl.pos = "lt")
corrplot(gpt, method = "number", type = "lower",
         tl.col = "n", tl.cex = 0.8, tl.pos = "n", number.cex = 0.3,
         add = T)


# 改色，添加一个自定义颜色
addcol <- colorRampPalette(c("CornflowerBlue", "white", "tomato"))#选择颜色
corrplot(gpt, method = "pie", type = "upper",col = addcol(100), 
         tl.col = "black", tl.cex = 0.8, tl.srt = 45,
         tl.pos = "lt")
corrplot(gpt, method = "number", type = "lower",col = addcol(100), 
         tl.col = "n", tl.cex = 0.8, tl.pos = "n", number.cex = 0.3,
         add = T)


# 添加统计学意义星号, 这里还加了一个AOE排序，也可以添加其他统计学数值，可以自己查看帮助文档
testRes = cor.mtest(gp, method="pearson", conf.level = 0.95)
corrplot(gpt, method = "color",#表示用颜色填充的方式来展示相关系数大小，颜色深浅代表相关性强弱
              col = addcol(100),#选择颜色
              tl.col = "black",#设置标签（tile labels，即变量名）的颜色为黑色
              tl.cex = 0.8,#标签字体大小调整为0.8倍默认大小
              tl.srt = 45,#标签倾斜角度设置为45度
              tl.pos = "lt",#标签位置设在左上角（left top）
              p.mat = testRes$p,#将显著性检验的结果矩阵赋值给p.mat，用于在图中标识显著性水平
              diag = T,#保留对角线上的元素，通常对角线上为1（完全相关），diag = F表示自相关去除
              type = 'upper',#只显示上三角部分的相关系数矩阵
              sig.level = c(0.001, 0.01, 0.05),#设置显著性水平，对应星号标记不同显著等级
              pch.cex = 0.8,#显著性符号（星号等）的大小调整为1.2倍默认大小
              insig = 'label_sig',#非显著相关系数以特定方式标注，即不显著的标识，表示不显著的相关性显示标签。 #显著性标注样式："pch", "p-value", "blank", "n", "label_sig"
              pch.col = 'grey20',#显著性符号的颜色设置为灰色
              order = 'AOE')#按照AOE顺序排列变量

corrplot(gpt, method = "number",#这次用数字直接表示相关系数的大小，替代之前的颜色填充
              type = "lower",#只显示下三角部分的相关系数数值
              col = addcol(100),#
              tl.col = "n",#
              tl.cex = 0.8,#
              tl.pos = "n",#不显示文本标签
              order = 'AOE',
              number.cex = 0.3,
              add = T)#这个参数表明此调用是在已有图形基础上添加内容，而不是创建新的图形。在这里就是在上一个相关系数矩阵的基础上，下方添加数字形式的相关系数信息。


# 结束绘图，关闭PDF文件
dev.off()

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

corrplot(
  corr,
  method = c("circle", "square", "ellipse", "number", "shade", "color", "pie"),
  type = c("full", "lower", "upper"),
  col = NULL,
  col.lim = NULL,
  bg = "white",
  title = "",
  is.corr = TRUE,
  add = FALSE,
  diag = TRUE,
  outline = FALSE,
  mar = c(0, 0, 0, 0),
  addgrid.col = NULL,
  addCoef.col = NULL,
  addCoefasPercent = FALSE,
  order = c("original", "AOE", "FPC", "hclust", "alphabet"),
  hclust.method = c("complete", "ward", "ward.D", "ward.D2", "single", "average",
    "mcquitty", "median", "centroid"),
  addrect = NULL,
  rect.col = "black",
  rect.lwd = 2,
  tl.pos = NULL,
  tl.cex = 1,
  tl.col = "red",
  tl.offset = 0.4,
  tl.srt = 90,
  cl.pos = NULL,
  cl.length = NULL,
  cl.cex = 0.8,
  cl.ratio = 0.15,
  cl.align.text = "c",
  cl.offset = 0.5,
  number.cex = 1,
  number.font = 2,
  number.digits = NULL,
  addshade = c("negative", "positive", "all"),
  shade.lwd = 1,
  shade.col = "white",
  p.mat = NULL,
  sig.level = 0.05,
  insig = c("pch", "p-value", "blank", "n", "label_sig"),
  pch = 4,
  pch.col = "black",
  pch.cex = 3,
  plotCI = c("n", "square", "circle", "rect"),
  lowCI.mat = NULL,
  uppCI.mat = NULL,
  na.label = "?",
  na.label.col = "black",
  win.asp = 1,
  ...


corrplot函数用于绘制相关系数矩阵的热图，其参数含义如下：

corr: 要绘制的相关系数矩阵。
method: 绘图方法，可以是"circle"（圆形）、"square"（正方形）、"ellipse"（椭圆）、"number"（数字）、"shade"（阴影）、"color"（颜色）、"pie"（饼图）中的一个。
type: 要显示的相关系数的类型，可以是"full"（全部显示）、"lower"（只显示下三角部分）、"upper"（只显示上三角部分）。
col: 相关系数的颜色。
col.lim: 颜色的范围限制。
bg: 背景颜色。
title: 图表的标题。
is.corr: 是否是相关系数矩阵。
add: 是否添加到现有图形上。
diag: 是否显示对角线上的相关系数。
outline: 是否显示外框。
mar: 图形边距。
addgrid.col: 网格线颜色。
addCoef.col: 相关系数的颜色。
addCoefasPercent: 是否将相关系数表示为百分比。
order: 排序方法，可以是"original"（原始顺序）、"AOE"、"FPC"、"hclust"（层次聚类）或"alphabet"（字母顺序）中的一个。
hclust.method: 层次聚类方法。
addrect: 要添加的矩形区域。
rect.col: 矩形的颜色。
rect.lwd: 矩形的线宽。
tl.pos: 标签位置。
tl.cex: 标签大小。
tl.col: 标签颜色。
tl.offset: 标签偏移量。
tl.srt: 标签旋转角度。
cl.pos: 颜色标签位置。
cl.length: 颜色标签长度。
cl.cex: 颜色标签大小。
cl.ratio: 颜色标签比例。
cl.align.text: 颜色标签对齐方式。
cl.offset: 颜色标签偏移量。
number.cex: 数字大小。
number.font: 数字字体。
number.digits: 数字小数位数。
addshade: 添加阴影的类型，可以是"negative"（负相关）、"positive"（正相关）、"all"中的一个。
shade.lwd: 阴影线宽。
shade.col: 阴影颜色。
p.mat: 相关系数的p值矩阵。
sig.level: 显著性水平。
insig: 不显著相关系数的表示方式。
pch: 不显著相关系数的符号。
pch.col: 符号颜色。
pch.cex: 符号大小。
plotCI: 置信区间的绘制方式。
lowCI.mat、uppCI.mat: 置信区间的上下限矩阵。
na.label: 缺失值标签。
na.label.col: 缺失值标签颜色。
win.asp: 窗口宽高比。
...: 其他参数传递给image函数。


## 参数介绍
mycol <- colorRampPalette(c("#06a7cd", "white", "#e74a32"), alpha = TRUE)
mycol2 <- colorRampPalette(c("#0AA1FF","white", "#F5CC16"), alpha = TRUE)
corrplot(corr, method = c('square'), type = c('lower'), 
               col = mycol2(100),#col是自己定义的颜色或色卡
               outline = 'grey', #是否为图形添加外轮廓线，默认FLASE，可直接TRUE或指定颜色向量
               order = c('AOE'), #排序/聚类方式选择："original", "AOE", "FPC", "hclust", "alphabet"
               diag = FALSE, #是否展示对角线结果，默认TRUE
               tl.cex = 1.2, #文本标签大小,即对角线文字大小
               tl.col = 'black', #文本标签颜色，即对角线文字颜色
               tl.pos = 'd', #仅在对角线显示文本标签
               tl.pos = 'n', #不显示文本标签
               tl.pos = "tp", #在左方和上方添加文本标签
               cl.pos = 'n', #不显示颜色图例
               addgrid.col= 'grey', #格子轮廓颜色
               addCoef.col = 'black', #在现有样式中添加相关性系数数字，并指定颜色
               number.cex = 0.8) #相关性系数数字标签大小

