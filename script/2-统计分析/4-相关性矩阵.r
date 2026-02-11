# 加载必要的库
library(PerformanceAnalytics)
library(Hmisc)
library(corrplot)
library(RColorBrewer)
library(grDevices)

# 读取数据
dd = read.csv("C:/Users/victo/Desktop/新建 Text Document.csv", sep = ",", header=T, row.names=1)

# 提取PC1, PC2, Latitude, Longtitude列
fixed_cols = c("Afanasievo", "Mongolia_N_North", "Haojiatai_LBIA", "Lubrak","Taiwan_Hanben","Hmong")
fixed_data = dd[, fixed_cols]

# 使用 rcorr 计算相关系数和p值矩阵
rcorr_result <- rcorr(as.matrix(dd)) # as.matrix 将数据转换为矩阵
re <- rcorr_result$r  # 相关系数矩阵
p <- rcorr_result$P  # p值矩阵

# 提取固定行和所有列的相关系数矩阵
re_fixed = re[fixed_cols, ]
p_fixed = p[fixed_cols, ]

# 设置显著性符号
stars <- ifelse(p_fixed < 0.001, "***", ifelse(p_fixed < 0.01, "**", ifelse(p_fixed < 0.05, "*", "")))

# 绘制相关性矩阵，并且只绘制固定的行和所有列
corrplot(re_fixed, method="color",
         type="full", # 绘制整个矩阵
         order="original", # 保持原有顺序
         #order = "alphabet",
         tl.col="black", # 标签颜色
         tl.cex=0.8, # 标签大小
         col=colorRampPalette(c("#20364F","#31646C","#4E9280","#96B89B",
                                "#DCDFD2","#ECD9CF","#D49C87","#B86265",
                                "#8B345E","#50184E"))(100),
         p.mat = p_fixed, # 提供 p 值矩阵
         insig = "label_sig", # 用显著性符号显示
         sig.level = c(0.001, 0.01, 0.05),
         pch = "*", # 使用 '*' 符号表示显著性
         pch.cex=0.5, # 显著性符号的大小
         pch.col = "#DCDFD2",
         cl.ratio = 1,
         cl.pos = "b") # 设置颜色条在右边
