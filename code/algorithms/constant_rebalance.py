'''
Constant rebalancing strategy

-TODO analyze optimal rebalancing frequency

'''
from .algorithm import *
import numpy as np
import logging

class Constant_rebalance(Algorithm):
    def setup(self,intial_portfolio,initial_period,model_params,data_column="close"):
        #todo consider how to format this for live trading.
        self.portfolio=intial_portfolio
        self.trade_frequency=model_params['trade_frequency']
        
        #to handle historical vs live, could be "close" or "last"
        self.data_column=model_params["data_column"]

    def format_market_data(self,market_data):
        '''
        Basically throw away anything that isn't the closing price
        Expecting data to come in as a tuple of the timestamp and a 2d data frame where the dimensions are assets and attributes
        
        '''
        return market_data.loc[:,self.data_column]



    def step(self,t,market_data):
        '''
            Check if enough time has passed since the last rebalancing, if so, rebalance
            Rebalance the postions held in each asset to be equal in value.
        '''
        if self.last_trade != None and (t-self.last_trade).hours/24.0 < self.trade_frequency:
            # we need to wait longer until rebalancing
            return 

        self.last_trade=t

        closing_prices= self.format_market_data(market_data)

        self.value=value_portfolio(closing_prices,self.portfolio)

        self.portfolio= self.value/closing_prices/closing_prices.shape[0]
        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
