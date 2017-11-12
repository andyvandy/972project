'''

Since we set up the data feed class to return a generator, it allows us to call run and 
have it run indefinitely.
'''
from algorithms.algorithm import *
import numpy as np
import pandas as pd
import logging

class Controller:
    '''
    General Class meant to be the glue between all of our algorithms and the data sources
    Takes in a datafeed which can feed in the historical  prices or potentially feed in live data.
    '''
    def __init__(self,algo_class,data_feed,model_params,verbose=False):
        logging.info('building Controller object')
        self.verbose=verbose #for debugging
        self.data_feed=data_feed
        self.closing_prices=pd.DataFrame()
        self.algorithm=algo_class(n_assets=data_feed.n_assets,verbose=verbose)
        self.model_params=model_params 
        self.last_market_data=None
        self.portfolio_history=[] #these are the raw postions
        self.portfolio_weight_history=[] #these are the percentage values of portfolio positions
        self.value_history=[]
        self.timestamps=[] #mostly for record creation and plotting
        self.asset_names=[] #used for ouput and for plotting
        

    def run(self):
        '''
        runs the simulation
        if this is slow we can enable storing of the results so that we don't haveto rerun this
        if we avoid printing we can benefit from tqdm's loading bar feature which is quite nice
        '''
        logging.info('Setting up algo with {} assets...'.format(self.data_feed.n_assets))
        
        #first period
        t0,first_period_data=next(self.data_feed.get_data())
        first_closing_prices=first_period_data.loc[:,'close']
        logging.info(first_closing_prices.keys())
        logging.info(dir(first_closing_prices))
        self.asset_names = first_closing_prices.keys()

        #todo make this better/ set up for live trading
        initial_portfolio=100/first_closing_prices/first_closing_prices.shape[0]

        self.algorithm.setup(initial_portfolio,first_period_data,model_params=self.model_params)

        self.portfolio_history.append(self.algorithm.portfolio)
        for t,market_period_data in self.data_feed.get_data():
            self.step(t,market_period_data)

    def step(self,t,market_period_data):
        '''
        Step through one period of the simulation. Add the current most recent price
        Allow the alogorithm to update its portfolio
        assert that the portfolio value doesn't change within a simulation step
        Log the new state
        '''
        if self.verbose:print("Simulation step # {}:".format(t))
        self.prices=market_period_data.loc[:,'close']    

        initial_value=value_portfolio(self.prices,self.algorithm.portfolio)
        self.algorithm.step(t,market_period_data)
        self.log_state(t,market_period_data)
        try:
            assert round(self.value_history[-1],8) == round(initial_value,8) # important to crash if this occurs
        except:
            print("initial value {} -> {} in same step!".format(initial_value, self.value_history[-1]))

        self.last_market_data=market_period_data

    def log_state(self,t,market_period_data):
        self.portfolio_history.append(self.algorithm.portfolio)
        value=value_portfolio(self.prices,self.algorithm.portfolio)
        self.portfolio_weight_history.append(self.algorithm.portfolio*self.prices/value)
        self.value_history.append(value)
        self.timestamps.append(t)

    def output_results(self):
        '''
        compute various performance measures such as the sharpe ratio.
        '''
        pass