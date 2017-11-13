'''
This class is used to feed in historical data to the algorithm for back testing purposes

load the data in from a series of Csvs, this is handy since a huge file with 100s of coins is slow to load..


'''
from data_feed import *
import os
import sqlite3
import pandas as pd
import logging

DATA_DIR=os.path.join("..","data") #todo move to a config file.

class HistoricalFeed(DataFeed):


    def __init__(self,pairs,folder,exchange="kraken",start=None,end=None,assets=None,verbose=0):
        '''
        Takes a list of pairs for which to load in the csv files
        For now kraken is default exchange simply because it gives us data that goes further back
        '''
        self.pairs=pairs
        pair_dfs={}
        for pair in pairs:
            pair_dfs[pair]=self.load_csv(filename=os.path.join(folder,exchange+"_"+pair.replace("/","_")+".csv"))
        
        self.df = pd.concat(pair_dfs,axis=1).dropna()    

        logging.debug("shape of data: {}".format(self.df.shape))
        #shape was weird, unclear why it isn't defaulting to multiindexing
        #logging.debug(self.df)


    def load_csv(self,filename):
        logging.debug("Historical Feed loading csv file {}...".format(filename))
        df=pd.read_csv(filename,low_memory=False,index_col='timestamp',parse_dates=True,header=0) 
        #logging.debug(df)
        return df

    def get_data(self):
        '''
        maybe this could be done more cleanly in one step but this works fine for now
        '''
        for row in self.df.iterrows():
            yield row
