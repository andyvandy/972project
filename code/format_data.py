"""
script to format the data into a pandas dataframe
"""
from os.path import join
import pandas as pd 

STOCKS=['AAPL','IBM','KO']
CSV_PATH=join('..', 'data')
stock_dfs=[pd.read_csv(join(CSV_PATH,stock+".csv"), index_col=0, parse_dates=True)['Adj Close'] for stock in STOCKS]


output_df=pd.concat(stock_dfs,axis=1).dropna()
output_df.columns=STOCKS
print(output_df)
output_df.to_csv(join(CSV_PATH,"market_data.csv"))

