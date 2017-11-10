'''
This class is used to feed in historical data to the algorithm for back testing purposes

Wehn we create the class we can setup a few different ways to laod the data in, 
this could be handy in that we won't need multiple processing steps
Also I didn't want to delete my sqlite loading function.

TODO:
    -implement filter based on start/stop date
    -implement filter based on asset list
'''
from data_feed import *
import os
import sqlite3
import pandas as pd
import logging

DATA_DIR=os.path.join("..","data") #todo move to a config file.

class HistoricalFeed(DataFeed):


    def __init__(self,filename,file_type="csv",start=None,end=None,assets=None,verbose=0):
        '''
        Takes in a sqlite file from which to read the historical data
        If no end or start dates are specified then all of the the observations are used.
        Also if no list of assets is provided then all of the assets in the file are used.
        '''
        
        if file_type.lower()=="csv":
            load_function=self.load_csv
        elif file_type.lower()=="sqlite":
            load_function=self.load_sqlite
        else:
            logging.warning('file loading method not found!')
            raise Exception('file load method not implemented')

        load_function(filename=filename,start=start,end=end,assets=assets,verbose=verbose)
        
        #logging.debug("shape of data: {}".format(self.df.shape))
        #shape was weird, unclear why it isn't defaulting to multiindexing
        self.n_assets=len(assets)

    def load_sqlite(self,filename,start=None,end=None,assets=None,verbose=0):
        conn = sqlite3.connect(os.path.join(DATA_DIR,filename)) 
        logging.debug("Historical Feed connected to sqlite3 file {}...".format(filename))
        with conn:
            self.df=pd.read_sql("SELECT * FROM data",conn ,index_col="index",parse_dates=["index"])
            if verbose: print("Data succesfully read from sqlite3 file  ({}) to pandas dataframe...".format(filename))

    def load_csv(self,filename,start=None,end=None,assets=None,verbose=0):
        logging.debug("Historical Feed loading csv file {}...".format(filename))
        self.df=pd.read_csv(filename,low_memory=False,index_col=0,parse_dates=True,header=[0,1]) # this could probably be more efficient
        self.df=self.df[assets].dropna()

    def get_data(self):
        '''
        maybe this could be done more cleanly in one step but this works fine for now
        '''
        for row in self.df.iterrows():
            yield row
