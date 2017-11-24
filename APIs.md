# 策略函数
initilize(context):初始化函数,在策略运行之初运行
before_trading(context):当日交易开始前运行
handle_bar(context,bar_map):每个交易日在每一个BAR上运行
after_trading(context):当日交易结束后运行

context:用户环境变量,与交易环境交互
bar_map:回测系统内部数据接口,用户可以获取行情数据

# 下单函数
order(ticker,amount,order_price=None):下单指定数量,amount正负控制方向
order_to(ticker,amount,order_price=None):下单到指定数量,amount正负控制方向
order_pct_to(ticker,amount,order_price=None):下单到指定资产比例,amount正负控制方向

# context

# Account查询方法
cash:返回当前现金
market_value:返回当前持仓市值
total_account_value:返回当前账户总资产值
get_position(ticker):当前持仓数量
get_position_cost(ticker):当前持仓成本
get_market_value(ticker):当前持仓市值

