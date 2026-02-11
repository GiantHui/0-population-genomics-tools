# 在开始之前请确保你已经安装了下列package
# 载入需要的package
library(ape)
library(igraph)
library(ggplot2)
library(pheatmap)
library(reshape2)
library(ggsci)
library(gridExtra)

# 设置工作路径，你需要把Fst文件和分组文件放到工作路径
setwd("C:/Users/LuzHu/Desktop/")

# 清除内存
rm(list=ls())

# 读取数据
mydata<-read.table("modern_contribution_matrix_normalized.csv",header=TRUE,sep=",", row.names = 1)
# group <-read.table("group.csv",header=TRUE,sep=",", row.names = 1)

# 创建绘图PDF
pdf("FstMatrix1.pdf", width=11, height=8.5)

# 绘制图像
pheatmap(mydata, 
        #  cluster_cols=TRUE, 
        #  cluster_rows=TRUE, 
         angle_col = c("45"),
         fontsize = 8,
         fontsize_row =8,
         fontsize_col =6,
        #  annotation_col = group, 
        #  annotation_row = group,
         cellwidth =8, 
         cellheight = 8, 
        #  cutree_cols=4,
        #  cutree_rows=4, 
         main = "FstMatrix",
         color = colorRampPalette(c("#40064B","#00847A","#D5D200"))(10000),
         display_numbers = matrix(ifelse(abs(mydata)> 50, "++", ifelse(abs(mydata)>=40,"+"," ")), nrow(mydata)))
# 结束绘图
dev.off()

# 换个样式
pheatmap(mydata, 
         cluster_cols=TRUE, 
         cluster_rows=TRUE, 
         angle_col = c("45"),
         fontsize = 8,
         fontsize_row =8,
         fontsize_col =6,
         annotation_col = group, 
         annotation_row = group,
         cellwidth =8, 
         cellheight = 8, 
         cutree_cols=4,
         cutree_rows=4, 
         main = "FstMatrix",
         color = colorRampPalette(c("#F8F8FF","#91D1C2FF","#3C5488FF"))(10000),
         display_numbers = matrix(ifelse(abs(mydata)> 50, "++", ifelse(abs(mydata)>=40,"+"," ")), nrow(mydata)))

# 换个样式
pheatmap(mydata,
         cluster_cols=TRUE,
         cluster_rows=TRUE,
         angle_col = c("45"),
         fontsize = 8,
         fontsize_row =8,
         fontsize_col =6,
         annotation_col = group,
         annotation_row = group,
         cellwidth =8,
         cellheight = 8,
         cutree_cols=4,
         cutree_rows=4,
         main = "FstMatrix",
         color = colorRampPalette(c("#20364F","#31646C","#4E9280","#96B89B","#DCDFD2","#ECD9CF","#D49C87","#B86265","#8B345E","#50184E"))(10000),
         display_numbers = matrix(ifelse(abs(mydata)> 50, "++", ifelse(abs(mydata)>=40,"+"," ")), nrow(mydata)))

# 换个样式
pheatmap(mydata,
         cluster_cols=TRUE,
         cluster_rows=TRUE,
         angle_col = c("45"),
         fontsize = 8,
         fontsize_row =8,
         fontsize_col =6,
         annotation_col = group,
         annotation_row = group,
         cellwidth =8,
         cellheight = 8,
         cutree_cols=4,
         cutree_rows=4,
         main = "FstMatrix",
         color = colorRampPalette(c("#023047","#126883","#279EBC","#90C9E6","#FC9E7F","#F75B41","#D52120"))(10000),
         display_numbers = matrix(ifelse(abs(mydata)> 50, "++", ifelse(abs(mydata)>=40,"+"," ")), nrow(mydata)))