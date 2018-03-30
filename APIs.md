# Config举例
config = {'base':
    {'start_date':'19900101',
     'end_date':'20200101',
     'capital':10000,
     'frequency':'1d',
     'universe':['000001']},
	 'source':'excel',
	 'file_path':''}

带有手续费设置的
config = {'base':
    {'start_date':'19900101',
     'end_date':'20200101',
     'capital':10000,
     'frequency':'1d',
     'universe':['000001']},
	 'source':'excel',
	 'file_path':'',
	 'fee':{'000001':[[1,1],[0,0.001],[0.003,0.003],[100,1]}}


## source
数据源,当前支持'excel','sql','bcolz'
excel和bcolz需要file_path

## 注意
universe必须是一个list.

# 策略函数
initilize(context):初始化函数,在策略运行之初运行  
before_trading(context):当日交易开始前运行  
handle\_bar(context,bar\_map):每个交易日在每一个BAR上运行  
after_trading(context):当日交易结束后运行  

context:用户环境变量,与交易环境交互  
bar_map:回测系统内部数据接口,用户可以获取行情数据  

# 下单函数
order(ticker,amount,order_price=None):下单指定数量,amount正负控制方向  
order\_to(ticker,amount,order_price=None):下单到指定数量,amount正负控制方向  
order\_pct\_to(ticker,amount,order_price=None):下单到指定资产比例,amount正负控制方向  

# context
dynamic_universe:当前动态股票池  
universe:股票池  
current_date:datetime,交易当天日期  
account:Account实例对象  

# bar_map
get_history(attr,n):attr为获取的属性，n为往后的交易天数,默认取不到当日  

# Account查询方法
cash:返回当前现金  
market_value:返回当前持仓市值  
total\_account\_value:返回当前账户总资产值  
get_position(ticker):当前持仓数量  
get\_position\_cost(ticker):当前持仓成本  
get\_market\_value(ticker):当前持仓市值  
get_weight: 当前持仓标的权重,不含现金,Series
