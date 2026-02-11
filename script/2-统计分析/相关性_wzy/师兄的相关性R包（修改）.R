install.packages("Rmisc")
install.packages("PerformanceAnalytics")
install.packages("corrplot")
install.packages("GGally")
library(PerformanceAnalytics)
library(Hmisc)
library(corrplot)
library(GGally)

library(Rmisc) 
library(corrplot)
library(ggcorrplot)
library(RColorBrewer)
library(grDevices)

#读取数据：使用read.csv函数从指定路径E:/research/5_YH3000/相关性/1.csv读取CSV文件，并将数据导入R环境中的数据框dd中。参数header=T意味着文件的第一行被视为列名，row.names = 1则指示将文件的第二列用作行名
dd=read.csv("D:/Y-chromosome/Affy/相关性分析/PC-经纬度-省份-单倍群.csv",header=T,row.names = 1)

#计算相关系数：计算数据框dd中所有列之间的皮尔逊相关系数，使用cor(dd)函数。这将返回一个相关系数矩阵
cor(dd)
#转换为矩阵：将数据框dd转换成矩阵格式，使用as.matrix(dd)函数。这是因为某些统计和数学运算在矩阵对象上更方便执行
dd = as.matrix(dd)

#计算完整观测相关系数：再次计算相关系数，但这次使用use = "complete.obs"参数，这意味着在计算相关系数时，只考虑没有缺失值的观测（即完全观测）。结果存放在re变量中
re = cor(dd,use = "complete.obs")

#计算p值：使用cor_pmat函数计算变量间的相关系数p值，并将结果四舍五入到小数点后10位，存储在变量p中。这里的method = "pearson"指明了使用的相关性测量方法为皮尔逊相关系数法
p <-round(cor_pmat(dd,method = "pearson"),10) 

#使用corrplot包绘制相关系数矩阵的上三角部分
corrplot(re, p.mat = p, #re：输入的相关系数矩阵，p.mat：对应的p值矩阵，用于标识显著性
         order = "original", #保持原始变量的顺序
         type="upper",#仅显示上三角区域的相关系数
         tl.col = "black",
         tl.cex = 0.8,
         tl.pos = "tp",#标签（tile labels）放置在顶部（top）
         insig="label_sig",#标注不显著的相关系数
         sig.level = c(.001, .01, .05),#设置显著性水平
         pch.cex = 0.5)#不显著关系的符号大小

#在上一步绘制的基础上，继续在同一张图上添加下三角区域，显示为数字形式的相关系数，并且禁用了对角线和类别标签
corrplot(re, add=TRUE,
         type="lower",
         method="number",#在现有图上添加下三角区域，显示为数字形式
         order="original",
         diag=FALSE,#不显示对角线上的值
         tl.col = "black",
         tl.cex = 0.8,
         tl.pos="n",#不显示标签（tile labels）
         cl.pos="n",#不显示类别标签（column labels）
         number.digits = 2,#设置数字的小数位数为2位
         number.cex = 0.3,
         number.font = NULL)#如果不特别指定字体，使用默认字体

