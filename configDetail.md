
	 
	 
config is a dict.
The general format of it is as follows

config = {'base':
    {'start_date':'19900101',
     'end_date':'20200101',
     'capital':10000,
     'frequency':'1d',
     'universe':['000001']}
	 'source':'excel'
	 'file_path':''}
	 
# base
## start_date
The start date of the backtest.
## end_date
The end date of the backtest.
## capital
The initial capital.
## frequency
The frequency of the backtest.

## universe
The universe of the backtest.

# source
The data source.

## excel
The excel format data.

## sql
The default sql database.

# file_path
If the source is 'excel', this parameter should be specified.
