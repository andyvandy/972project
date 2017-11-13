'''
This class loads in live data for us to trade with

Unsure wheter multiple exchange objects should be maintained or if this class is supposed to share a global object

TODO:
    -bid ask
    -multiple exchanges
    -extra data
    -async*******
        -use asyncio.gather to load the tickers we need/other data asynchronously from multiple sources

'''

from data_feed import *
import os
import sqlite3
import pandas as pd
import logging
import asyncio
import time
import ccxt
import datetime

#todo reevaluate how to do this better?
TIMEFRAMES={
    "1m":60*1000,
    "5m":5*60*1000,
    "30m":30*60*1000,
    "1h":60*60*1000,
    "6h":6*60*60*1000,
    "12h":12*60*60*1000,
    "1d":24*60*60*1000,
}

class LiveFeed(DataFeed):

    def __init__(self,pairs,exchange="bitfinex",frequency="1m"):
        logging.info("Initializing live feed object connected to {} polling at {} frequency.".format(exchange,frequency))

        self.pairs=pairs
        self.exchange =getattr(ccxt, exchange)({
            'rateLimit': 3000,
            'enableRateLimit': True,
            # 'verbose': True,
            })
        self.markets=self.exchange.load_markets()
        self.frequency=frequency
        self.retry_time=10
        self.fields=["last","bid","ask"]

    def get_data(self):
        '''
        This generator yields in an infinite loop to continously provide data as requested
        We want to generate data close to the frequency requested.
        todo make this async on a timed loop. not too tricky.
        '''
        last_timestamp=self.exchange.milliseconds()
        yield datetime.datetime.fromtimestamp(last_timestamp/1000.0),self.get_formatted_data()
        
        while True:
            #logging.debug("last_timestamp:{} , timesince:{}, freq:{} ".format(last_timestamp,self.exchange.milliseconds()-last_timestamp,TIMEFRAMES[self.frequency]))
            if self.exchange.milliseconds()-last_timestamp < TIMEFRAMES[self.frequency]:
                #sleep and check again later if it's time yet to yield some more data
                time.sleep(min(10,(self.exchange.milliseconds()-last_timestamp)/1000))
                continue
            last_timestamp=self.exchange.milliseconds()
            yield datetime.datetime.fromtimestamp(last_timestamp/1000.0),self.get_formatted_data()


    def get_formatted_data(self):
        success=False
        while not(success):
            try:
                all_tickers= self.exchange.fetch_tickers()
                success=True
            except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
                logging.warning('Got an error {} ,retrying in {}'.format(type(error).__name__, error.args,self.retry_time))
                time.sleep(self.retry_time)
        index=pd.MultiIndex.from_product([self.pairs,self.fields])

        ticker_data= [data[field]  for (pair,data) in all_tickers.items() for field in self.fields if pair in self.pairs]
        df=pd.Series(ticker_data,index=index)
        print(df)
        return df