# 加载必要的库
library(PerformanceAnalytics)
library(Hmisc)
library(corrplot)
library(GGally)
library(Rmisc) 
library(ggcorrplot)
library(RColorBrewer)
library(grDevices)

# 读取数据
dd = read.csv("C:/Users/victo/Desktop/新建 Text Document.txt",sep = "\t", header=T, row.names=1)

# 计算相关系数
cor(dd)

# 转换为矩阵
dd = as.matrix(dd)

# 计算完整观测相关系数
re = cor(dd, use="complete.obs")

# 计算p值
p = round(cor_pmat(dd, method="pearson"), 10)

# 设定PDF的尺寸
# pdf("C:/Users/victo/Desktop/output_fixed.pdf", width=20, height=14)  # 设置PDF宽度和高度

# 调整绘图边距
# par(mar=c(1, 1, 1, 1))  # 设置绘图边距，确保内容不会被截掉

# 指定颜色渐变
color_palette <- colorRampPalette(c("#20364F","#31646C","#4E9280","#96B89B",
                                    "#DCDFD2","#ECD9CF","#D49C87","#B86265",
                                    "#8B345E","#50184E"))(100)

# 绘制上三角区域的相关系数矩阵
corrplot(re, p.mat=p,
         order="original", # 保持原有的排序顺序
         type="upper", # 将部分放在上边
         tl.col="black", # 标签颜色
         tl.cex=0.8, # 标签大小
         tl.pos="tp",
         insig="label_sig",
         sig.level=c(.001, .01, .05),
         pch.cex=0.8,  # 调整不显著关系的符号大小
         col=color_palette)  # 使用指定的颜色

# 在上一步绘制的基础上，继续绘制下三角区域
corrplot(re, add=TRUE,
         type="lower",
         mar=c(0, 0, 0, 0),  # 设置边距，确保内容不会被截掉
         method="number", # 用数字表示
         order="original", # 保持原有排序
         diag=FALSE,
         tl.col="black",
         tl.cex=0.8,
         tl.pos="n",
         cl.pos="n",
         number.digits=2,
         number.cex=0.6,  # 调整数字大小
         number.font=1,  # 指定字体
         col=color_palette,
         addCoef.col=NA)  # 不设置addCoef.col

# 自定义绘制数字背景
for(i in 1:nrow(re)) {
  for(j in 1:i) {
    value_color <- color_palette[round((re[i, j] + 1) / 2 * 99) + 1]
    rect(xleft=j-0.5, ybottom=nrow(re)-i+0.5, xright=j+0.5, ytop=nrow(re)-i+1.5,
         col=value_color, border=NA)
    
    # 计算背景颜色的亮度
    bg_col <- col2rgb(value_color) / 255
    brightness <- sqrt(0.299 * bg_col[1]^2 + 0.587 * bg_col[2]^2 + 0.114 * bg_col[3]^2)
    
    # 根据亮度选择字体颜色
    text_color <- ifelse(brightness > 0.5, "black", "white")
    
    text(j, nrow(re)-i+1, round(re[i, j], 2), col=text_color, cex=0.6)
  }
}

# 关闭PDF设备
dev.off()

# # 加载必要的库
# library(PerformanceAnalytics)
# library(Hmisc)
# library(corrplot)
# library(GGally)
# library(Rmisc)
# library(ggcorrplot)
# library(RColorBrewer)
# library(grDevices)

# # 读取数据
# dd = read.csv("C:/Users/victo/Desktop/新建 Text Document.txt", sep = "\t", header=T, row.names=1)

# # 提取PC1, PC2, Latitude, Longtitude列
# fixed_cols = c("Afanasievo", "Mongolia_N_North", "Haojiatai_LBIA", "Lubrak","Taiwan_Hanben","Hmong")
# fixed_data = dd[, fixed_cols]

# # 将列名分为群组和单倍型组
# group_cols = colnames(dd)[grepl("_", colnames(dd))]
# haplotype_cols = colnames(dd)[!grepl("_", colnames(dd)) & !colnames(dd) %in% fixed_cols]

# # 提取群组和单倍型数据
# group_data = dd[, group_cols]
# haplotype_data = dd[, haplotype_cols]

# # 计算群组和单倍型的相关系数矩阵
# re_group = cor(group_data, use="complete.obs")
# zero_variance_cols = sapply(haplotype_data, function(col) sd(col, na.rm = TRUE) == 0)
# # 打印常数列名称
# if (any(zero_variance_cols)) {
#   cat("具有零标准差的列：", names(haplotype_data)[zero_variance_cols], "\n")
# }
# # 从数据中移除这些列
# haplotype_data_filtered = haplotype_data[, !zero_variance_cols]
# # 计算群组和单倍型的相关系数矩阵
# re_group = cor(group_data, use="complete.obs")
# re_haplotype = cor(haplotype_data_filtered, use="complete.obs")

# # 层次聚类等操作
# hc_group = hclust(as.dist(1 - re_group))
# hc_haplotype = hclust(as.dist(1 - re_haplotype))

# # 重新排序列名
# group_order = group_cols[hc_group$order]
# haplotype_order = haplotype_cols[hc_haplotype$order]

# # 重新排列数据框
# dd_reordered = dd[, c(fixed_cols, group_order, haplotype_order)]

# # 计算完整观测相关系数
# re = cor(dd_reordered, use="complete.obs")

# # 计算p值
# p = round(cor_pmat(dd_reordered, method="pearson"), 10)

# # 设定PDF的尺寸
# # pdf("C:/Users/victo/Desktop/output_fixed.pdf", width=20, height=14)  # 设置PDF宽度和高度

# # 调整绘图边距
# par(mar=c(1, 1, 1, 1))  # 设置绘图边距，确保内容不会被截掉

# # 指定颜色渐变
# color_palette <- colorRampPalette(c("#20364F","#31646C","#4E9280","#96B89B",
#                                     "#DCDFD2","#ECD9CF","#D49C87","#B86265",
#                                     "#8B345E","#50184E"))(100)

# # 绘制上三角区域的相关系数矩阵
# corrplot(re, p.mat=p,
#          order="original", # 保持原有的排序顺序
#          type="upper", # 将部分放在上边
#          tl.col="black", # 标签颜色
#          tl.cex=0.8, # 标签大小
#          tl.pos="tp",
#          insig="label_sig",
#          sig.level=c(.001, .01, .05),
#          pch.cex=0.8,  # 调整不显著关系的符号大小
#          col=color_palette, # 使用指定的颜色
#          #outline=TRUE, # 添加边框
#          #addgrid.col="#BDF7F6"
#          )  # 设置边框颜色

# # 在上一步绘制的基础上，继续绘制下三角区域
# corrplot(re, add=TRUE,
#          type="lower",
#          mar=c(0, 0, 0, 0),  # 设置边距，确保内容不会被截掉
#          method="number", # 用数字表示
#          order="original", # 保持原有排序
#          diag=FALSE,
#          tl.col="black",
#          tl.cex=0.8,
#          tl.pos="n",
#          cl.pos="n",
#          number.digits=2,
#          number.cex=0.6,  # 调整数字大小
#          number.font=1,  # 指定字体
#          col=color_palette,
#          addCoef.col=NA, # 不设置addCoef.col
#          #outline=TRUE, # 添加边框
#          #addgrid.col="#BDF7F6"
#          )  # 设置边框颜色

# # 自定义绘制数字背景
# for(i in 1:nrow(re)) {
#   for(j in 1:i) {
#     value_color <- color_palette[round((re[i, j] + 1) / 2 * 99) + 1]
#     rect(xleft=j-0.5, ybottom=nrow(re)-i+0.5, xright=j+0.5, ytop=nrow(re)-i+1.5,
#          col=value_color, border=NA)
    
#     # 计算背景颜色的亮度
#     bg_col <- col2rgb(value_color) / 255
#     brightness <- sqrt(0.299 * bg_col[1]^2 + 0.587 * bg_col[2]^2 + 0.114 * bg_col[3]^2)
    
#     # 根据亮度选择字体颜色
#     text_color <- ifelse(brightness > 0.5, "black", "white")
    
#     text(j, nrow(re)-i+1, round(re[i, j], 2), col=text_color, cex=0.6)
#   }
# }

# # 关闭PDF设备
# # dev.off()


