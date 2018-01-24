# vectra
策略回测。
仅提供交易过程中的所有记录(账户、订单),暂不提供统计指标计算.

# Installation
1. 向site-packages中添加VectorTrader路径文件pth.
2. 安装requirments中的需求

# About Excel format data source
要求Excel数据表格式如下
列为trade\_date,open\_price,high\_price,low\_price,close\_price,amount,volume,trade\_code
trade\_date时间格式要求能够被pd.read_excel识别。
