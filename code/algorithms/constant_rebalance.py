'''
Constant rebalancing strategy

-TODO make this algorithm behave properly in the face of already having a portfolio initialized

'''
from .algorithm import *
import numpy as np

class Constant_rebalance(Algorithm):
    def setup(self,intial_portfolio,model_params):
        #todo consider how to format this for live trading.
        self.portfolio=intial_portfolio


    def format_market_data(self,market_data):
        '''
        Basically throw away anything that isn't the closing price
        Expecting data to come in as a tuple of the timestamp and a 2d data frame where the dimensions are assets and attributes
        
        '''
        return market_data.loc[:,'close']



    def step(self,t,market_data):
        '''
            Look at the most recent period and rebalance accordingly.
        '''
        closing_prices= self.format_market_data(market_data)

        
        self.value=value_portfolio(closing_prices,self.portfolio)

        self.portfolio= self.value/closing_prices/closing_prices.shape[0]
        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
