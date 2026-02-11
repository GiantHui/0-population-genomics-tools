install.packages("linkET")
install.packages("ggcor")
devtools::install_git("https://gitee.com/dr_yingli/ggcor")
devtools::install_github("houyunhuang/ggcor")
setwd("D:/Rstudio/R")#设置绘图默认路径，可根据自己喜好
set.seed(123)  # 随机种子
library(corrplot)#加载相关热图包
library(vegan)#加载vegan包
library(ggcor)#加载vegan包
data("varechem")#加载vegan内置数据-理化数据
data("varespec")#加载vegan内置数据-物种数据
#查看数据

varechem=read.csv("E:/research/5_YH3000/相关性/mantel/单倍群组成.csv",header=T,row.names = 1)
varespec=read.csv("E:/research/5_YH3000/相关性/mantel/mantel.csv",header=T,row.names = 1)
head(varechem)
head(varespec)
cor_plot<-cor(varechem)
corrplot(cor_plot,method = "color" ,type = "upper",addrect = 1,insig="blank",rect.col = "blue",rect.lwd = 2)
mt<-function(varespec,varechem){#如果换成自己的数据时，对照将varespec换成物种数据，varechem换成理化数据框名
  library(vegan)
  library(dplyr)
  vars <- colnames(varechem)#这里的varechem换成自己的理化数据框名
  models<-list()
  for (i in seq_along(vars)){
    otu_bray<-vegdist(varespec,method = "bray")#将varespec换成自己的物种数据框名
    env_dis<-vegdist(varechem[vars[i]],method = "euclidean")#将varechem换成自己的理化数据框名
    model <- mantel(otu_bray,env_dis, permutations=999)
    name <- vars[i]
    statistic <- model$statistic
    signif <- model$signif
    models[[i]] <- data.frame(name = name, statistic = statistic, signif = signif, row.names = NULL)
  }
  models %>% bind_rows()
}#这里定义了一个提取Mantel tests的R和p值
Total<-mt(varespec,varechem)#提取总物种数据与环境因子数据间的R和p值
mantRpsub1<-mt(varespec[,1:22],varechem)#将1到22个物种定义为一个亚组,并计算物种数据与环境因子数据间的R和p值，比如本文图1中的Gene functional composition
mantRpsub2<-mt(varespec[,-(1:22)],varechem)#与上面的亚组定义类似
set.seed(123)
n <- ncol(varechem)
#grp <- c('Total', 'Sub1', 'Sub2') # 分组名称
grp <- ('Total') # 分组名称
#subx <- c(-3, -1, 1) # 分组的X坐标
#suby <- c(7, 4, 1) # 分组的Y坐标
subx <- (-1) # 分组的X坐标
suby <- (4) # 分组的Y坐标
df <- data.frame(grp = rep(grp, each = n), # 分组名称，每个重复n次
                 subx = rep(subx, each = n), # 组X坐标，每个重复n次
                 suby = rep(suby, each = n), # 组Y坐标，每个重复n次
                 x = rep(0:(n - 1) - 0.5, 3), # 变量连接点X坐标
                 y = rep(n:1, 3) # 变量连接点Y坐标
)
#df2 <-rbind(mantRpTotal, mantRpsub1, mantRpsub2)
df2 <-rbind(Total)
df_segment<-cbind(df,df2)
df_segment <- df_segment %>% 
  mutate(
    lcol = ifelse(signif <= 0.001, '#1B9E77', NA), 
    # p值小于0.001时，颜色为绿色，下面依次类推
    lcol = ifelse(signif > 0.001 & signif <= 0.01, '#88419D', lcol),
    lcol = ifelse(signif > 0.01 & signif <= 0.05, '#A6D854', lcol),
    lcol = ifelse(signif > 0.05, '#B3B3B3', lcol),
    lwd = ifelse(statistic >= 0.3,6, NA),
    # statistic >= 0.3 时，线性宽度为6，下面依次类推
    lwd = ifelse(statistic >= 0.15 & statistic < 0.3, 3, lwd),
    lwd = ifelse(statistic < 0.15, 1, lwd))
corrplot(cor(varechem),method = "color",type = "upper", addrect = 1,insig="blank",rect.col = "blue",rect.lwd = 2)#绘制右边热图

segments(df_segment$subx, df_segment$suby, df_segment$x, df_segment$y, lty = 'solid', lwd = df_segment$lwd, col = df_segment$lcol, xpd = TRUE)
guides(fill = guide_colorbar(title = "correlation", order = 1),#图例相关设置
       size = guide_legend(title = "Mantel's r",order = 2),
       color = guide_legend(title = "Mantel's p", order = 3),
       linetype = "none")
points(subx, suby, pch = 24, col = 'blue', bg = 'blue', cex = 2, xpd = TRUE)#点的位置和形状
text(subx - 0.5, suby, labels = grp, adj = c(0.8, 0.5), cex = 1.2, xpd = TRUE)#文本位置






#ggcor版
devtools::install_git("https://gitee.com/dr_yingli/ggcor") #ggcor目前没有进官方的R包库，可以用这行代码安装
#如果安装不上，可点击这个链接: https://pan.baidu.com/s/1GuN404YPDaPA-MMu_auImA 提取码: ge1p 下载后解压了的ggcor文件夹放到R的library目录下即可
library(vegan)
library(ggcor)
mantel <- mantel_test(varespec, varechem, #调用vegan包中的内置数据，见上方解释
                      spec.select = list(Spec01 = 1:7,#依次定义四种物种作为Mantel的分析对象
                                         Spec02 = 8:18,
                                         Spec03 = 19:37,
                                         Spec04 = 38:44)) %>% 
  mutate(rd = cut(r, breaks = c(-Inf, 0.2, 0.4, Inf),
                  labels = c("< 0.2", "0.2 - 0.4", ">= 0.4")),#定义Mantel的R值范围标签，便于出图
         pd = cut(p.value, breaks = c(-Inf, 0.01, 0.05, Inf),
                  labels = c("< 0.01", "0.01 - 0.05", ">= 0.05")))#定义Mantel检验的p值范围标签，便于出图
quickcor(varechem, type = "upper") +#绘制理化数据热图
  geom_square() +#定义成方块状
  anno_link(aes(colour = pd, size = rd), data = mantel) +#定义连线
  scale_size_manual(values = c(0.5, 1, 2))+
  guides(size = guide_legend(title = "Mantel's r",#定义图例
                             order = 2),
         colour = guide_legend(title = "Mantel's p", 
                               order = 3),
         fill = guide_colorbar(title = "Pearson's r", order = 4))

