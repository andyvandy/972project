'''
script to download data from yahoo finance
'''

import os
import pandas as pd
import pandas_datareader.data as web # need to install seperatel from pandas
import datetime
from tqdm import *

def main():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2014, 12, 31)
    companies_df=pd.DataFrame.from_csv('../data/companylist.csv')
    for ticker in tqdm(companies_df.index):
        try:
            save_stock_close_data(ticker,start,end)
        except:
            pass

def save_stock_close_data(ticker,start,end):
    f = web.DataReader(ticker, 'yahoo', start, end)[['Adj Close']] # only want adjusted close
    f.to_csv(os.path.join("../data","stocks",ticker+".csv"))

if __name__ =="__main__":
    main()


    ### Test Edit 