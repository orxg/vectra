# vectra
策略回测。
仅提供交易过程中的所有记录(账户、订单),暂不提供统计指标计算.

# Installation
1. 向site-packages中添加VectorTrader路径文件pth.
2. 安装requirments中的需求

# About Excel format data source
要求Excel数据如下
1. 列为trade\_date,open\_price,high\_price,low\_price,close\_price,amount,volume,trade\_code
2. trade\_date时间格式要求能够被pd.read_excel识别。
3. volume为成交量股数,amount为成交金额,单位是元.但是,在策略当中,下单数量用参数amount代表.
4. 无交易数据的处理: 采用空值

# Some Features
## Matching Regime
1. 卖出下单数量超过持仓数量,作为清仓处理
2. 买入下单金额(含手续费)超出可用现金,直接拒单

# Next Plan
1. 增加订单反馈机制,对于未成交的被拒订单考虑相应的应对机制
2. 在1的基础上搭建一个仅基于目标仓位数据来进行策略回测的程序,这样对于类似多因子,仅仅给出目标仓位的策略回测起来就非常快