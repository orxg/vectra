# vectra
策略回测

# Installation
1. 向site-packages中添加VectorTrader路径文件pth.
2. 安装requirments中的需求

# About Excel Format Data Source
要求Excel数据如下
1. 列为trade\_date,open\_price,high\_price,low\_price,close\_price,amount,volume,trade\_code
2. trade\_date时间格式要求能够被pd.read_excel识别。
3. volume为成交量股数,amount为成交金额,单位是元.但是,在策略当中,下单数量用参数amount代表.
4. 无交易数据的处理: 采用空值

# Backtest Based On Historical Weight
基于仓位进行回测的机制,调用函数run_weight.
历史仓位数据目前支持excel数据,格式为  

trade_date sec_1 sec_2   
20180131	0.2   0.8    
20180228	0.5	  0.5  

注意,列名与日期必须严格按照上述格式.
# Benchmark
在config中提供benchmark数据excel格式路径地址,可以绘制基准收益率,以及相对收益率.  
benchmark的Excel数据格式如下  
trade_date close_price  
20180101	12  
20180102	13  
.....

# Some Features
## Matching Regime
1. 卖出下单数量超过持仓数量,作为清仓处理
2. 买入下单金额(含手续费)超出可用现金,按最大可成交数量成交

## Transaction Fee
可以通过config,手动指定相关交易费用,在不指定的情况下,默认按照股票的交易费用进行处理。
需要指定买卖两方面参数,下图为默认参数  
![Alt text]transaction_fee.PNG

其中 
1. transfer\_fee\_on:过户费仅有0和1,即有和无两种  
2. tax\_rate:税收按照给出的税率计算,即成交金额乘以税率  
3. commission\_fee\_rate:交易佣金费率若不为0,则根据交易金额与费率乘积计算,最低为5;为0时则默认为0
4. min\_amount:最小成交数量

在config中的设置为关键字 'fee',比如  
config = {'base':
    {'start_date':'19900101',
     'end_date':'20200101',
     'capital':10000,
     'frequency':'1d',
     'universe':['000001']},
	 'source':'excel',
	 'file_path':'',
	 'benchmark_path':'',
	 'fee':
	 {'000001':[1,1,0,0.001,0.003,0.003,100,1]}}
其中key为标的,值为一个根据上图格式的list.  
对应的值为按照上图中从上到下，从左到右的顺序。

# Next Plan
1. 增加策略跟踪
