##Set working directory

install.packages("geodist")
install.packages("ape")
install.packages("vegan")
setwd("E:/research/5_YH3000/Beast")
library(geodist)
library(ape)
library(vegan)

x <- as.DNAbin(read.dna("E:/research/5_YH3000/Beast/samples.fasta", format = "fasta", as.character = TRUE))
x.dist <- dist.dna(x)
x.dist.matrix <- as.dist(as.matrix(x.dist))

y <- read.csv("E:/research/5_YH3000/Beast/mantel.csv", row.names = 1)
y.dist.matrix <- as.dist(geodist(y, measure = "haversine"))
names(y.dist.matrix) <- names(x.dist.matrix)

xy.mantel <- mantel(x.dist.matrix, y.dist.matrix, permutations = 10000)



##代码释义

#这段代码主要是用于分析DNA序列数据和地理距离数据之间的相关性。

1.install.packages("geodist")：安装 geodist 包，用于计算地理距离。
2.install.packages("ape")：安装 ape 包，用于处理进化生物学数据。
3.install.packages("vegan")：安装 vegan 包，用于生态学和环境科学中的数据分析。
4.setwd("E:/research/5_YH3000/Beast")：设置工作目录为 "E:/research/5_YH3000/Beast"，即所有后续操作的文件路径将在这个目录下进行。
5.library(geodist)、library(ape)、library(vegan)：加载之前安装的三个包，以便后续使用这些包中的函数。
6.x <- as.DNAbin(read.dna("E:/research/5_YH3000/Beast/samples.fasta", format = "fasta", as.character = TRUE))：从 FASTA 格式的 DNA 序列文件中读取序列数据，并将其转换为 DNAbin 格式的对象 x。
7.x.dist <- dist.dna(x)：计算 DNA 序列数据的距离矩阵。
8.x.dist.matrix <- as.dist(as.matrix(x.dist))：将距离对象转换为矩阵形式。
9.y <- read.csv("E:/research/5_YH3000/Beast/mantel.csv", row.names = 1)：从 CSV 文件中读取地理距离数据，并将其存储在对象 y 中，其中 row.names = 1 表示使用第一列作为行名。
10.y.dist.matrix <- as.dist(geodist(y, measure = "haversine"))：使用 geodist 包中的 geodist 函数计算地理距离数据的距离矩阵，并将其转换为距离对象。
11.names(y.dist.matrix) <- names(x.dist.matrix)：给 y.dist.matrix 距离矩阵的行和列命名，以匹配 x.dist.matrix 的行和列。
12.xy.mantel <- mantel(x.dist.matrix, y.dist.matrix, permutations = 10000)：使用 mantel 函数计算两个距离矩阵之间的 Mantel 相关系数，并指定进行 10000 次置换以计算 p 值。

#这段代码的目的是通过 Mantel 测试来检验DNA序列数据和地理距离数据之间的相关性。



