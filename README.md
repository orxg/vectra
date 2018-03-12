# vectra
策略回测。

# Installation
1. 向site-packages中添加VectorTrader路径文件pth.
2. 安装requirments中的需求

# About Excel Format Data Source
要求Excel数据如下
1. 列为trade\_date,open\_price,high\_price,low\_price,close\_price,amount,volume,trade\_code
2. trade\_date时间格式要求能够被pd.read_excel识别。
3. volume为成交量股数,amount为成交金额,单位是元.但是,在策略当中,下单数量用参数amount代表.
4. 无交易数据的处理: 采用空值

# Backtest Based On Historic Weight
基于仓位进行回测的机制,调用函数run_weight.
历史仓位数据目前支持excel数据,格式为  

trade_date sec_1 sec_2   
20180131	0.2   0.8    
20180228	0.5	  0.5  

注意,列名与日期必须严格按照上述格式.

# Some Features
## Matching Regime
1. 卖出下单数量超过持仓数量,作为清仓处理
2. 买入下单金额(含手续费)超出可用现金,按最大可成交数量成交

# Next Plan
1. 增加订单反馈机制,对于未成交的被拒订单考虑相应的应对机制
