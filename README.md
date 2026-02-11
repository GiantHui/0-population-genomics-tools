# 0-population-genomics-tools
A collection of scripts and utilities for population genomics data processing and analysis.

这是一个专为群体遗传学（Population Genomics）设计的脚本和工具集合，旨在简化数据处理、分析和可视化流程。

## 📁 项目结构

为了保持仓库整洁，所有脚本均按功能分类存放于 `scripts/` 目录下：

* **`scripts/`**: 核心脚本根目录
    * `9-数据处理`: 包含 经纬度、矩阵等预处理脚本。
    * `8-Arlequin`: 包含 Arlequin软件使用时的计算工具。
    * `7-曼哈顿图`: 用于生成曼哈顿图的可视化脚本。


## 🚀 快速开始

### 环境依赖
在使用这些脚本之前，请确保你的系统中已安装以下软件：
* Python 3.x 或 R (取决于具体脚本)
* BCFtools / SAMtools

### 使用示例
进入对应目录并运行脚本，例如：
```bash
python scripts/data_processing/your_script.py --input test.vcf --output filtered.vcf
```
