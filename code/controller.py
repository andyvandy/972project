'''

Since we set up the data feed class to return a generator, it allows us to call run and 
have it run indefinitely.

Note: we need to make sure that for live feed purposes we only log for a certain window or we'll run out of memory

'''
from algorithms.algorithm import *
import numpy as np
import pandas as pd
import logging
import os 

class Controller:
    '''
    General Class meant to be the glue between all of our algorithms and the data sources
    Takes in a datafeed which can feed in the historical  prices or potentially feed in live data.
    '''
    def __init__(self,algo_class,data_feed,model_params,price_column_name="close",verbose=False,log_folder=None):
        logging.info('building Controller object')
        self.verbose=verbose #for debugging
        self.data_feed=data_feed
        self.closing_prices=pd.DataFrame()
        self.algorithm=algo_class(n_assets=len(data_feed.pairs),verbose=verbose)
        self.model_params=model_params 
        self.last_market_data=None
        self.portfolio_history=[] #these are the raw postions
        self.portfolio_weight_history=[] #these are the percentage values of portfolio positions
        self.value_history=[]
        self.timestamps=[] #mostly for record creation and plotting
        self.asset_names=[] #used for ouput and for plotting
        self.price_column_name=price_column_name #could be "close" for hist or "last" for live
        self.actions_history=[] #used to track trade actions
        self.actions=[] #used to track trade actions

        #check here if you're lost https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
        self.log_folder=log_folder
        self.logger = logging.getLogger('controller_logger')
        self.logger.setLevel(level=logging.DEBUG) #todo make this configurable in main.py
        if self.log_folder is None:#log to stdout in this case
            handler=logging.StreamHandler()
        else:
            handler=logging.FileHandler(filename=os.path.join(self.log_folder,"{}.log".format(self.algorithm.__class__.__name__)))
        self.logger.addHandler(handler)
        self.reset_logs()#temporary
          
    def run(self):
        '''
        runs the simulation
        if this is slow we can enable storing of the results so that we don't haveto rerun this
        if we avoid printing we can benefit from tqdm's loading bar feature which is quite nice
        '''
        logging.info('Setting up algo with {} assets...'.format(len(self.data_feed.pairs)))
        
        #first period
        t0,first_period_data=next(self.data_feed.get_data())
        first_closing_prices=first_period_data.loc[:,self.price_column_name]
        logging.info(first_closing_prices.keys())
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
        self.prices=market_period_data.loc[:,self.price_column_name]    

        initial_value=value_portfolio(self.prices,self.algorithm.portfolio)
        self.algorithm.step(t,market_period_data)
        self.execute()
        self.log_history(t,market_period_data)
        try:
            assert round(self.value_history[-1],8) == round(initial_value,8) # important to crash if this occurs
        except:
            print("initial value {} -> {} in same step!".format(initial_value, self.value_history[-1]))

        #log results of this step
        self.log_step(t,market_period_data)

        #run end of period update stuff
        self.last_market_data=market_period_data

    def execute(self):
        '''
        Perform actions such that we translate the new portfolio selection into market actions
        TODO
        '''
        self.actions=[{"type":"TODO"}]

    def log_history(self,t,market_period_data):
        #log the historical values for analysis or backtested stratgies largely
        self.portfolio_history.append(self.algorithm.portfolio)
        value=value_portfolio(self.prices,self.algorithm.portfolio)
        self.portfolio_weight_history.append(self.algorithm.portfolio*self.prices/value)
        self.value_history.append(value)
        self.actions_history.append(self.actions)
        self.timestamps.append(t)


    def log_step(self,t,market_period_data):
        '''
        log period market data as well as actions the algo has taken to a outputstream. 
        USe the built in logger to keep this easy/efficient
        TODO: 
            -actually make this print out nicely later
            
        '''
        header="\n{timestamp}-- Trade log for: {algo}\n".format(timestamp=t,algo=self.algorithm.__class__.__name__)
        prices="{}\n".format(market_period_data)
        portfolio="  portfolio:\n"+"".join(["{:>4}\n".format(position) for position in self.algorithm.portfolio])
        value="  value:\n{:>4}\n".format(self.value_history[-1])
        actions="  actions:\n{}\n".format(self.actions)
        record="".join([header,prices,portfolio,value,actions])
        self.logger.info(record)


        if self.log_folder is not None:
            #log the value
            with open(os.path.join(self.log_folder,"value_history_{}.csv".format(self.algorithm.__class__.__name__)),"a") as f:
                f.write("{t},{value}\n".format(t=t,value=self.value_history[-1]))

            #log the portfolio weights
            with open(os.path.join(self.log_folder,"weight_history_{}.csv".format(self.algorithm.__class__.__name__)),"a") as f:
                f.write("{t},{weights}\n".format(t=t,weights=",".join([str(weight) for weight in self.portfolio_weight_history[-1]])))

    def reset_logs(self):
        #-currently going to wipe the logs at the start since the portoflio initialization 
        # resets the portfolio each time which ruins the graph and data
        with open(os.path.join(self.log_folder,"{}.log".format(self.algorithm.__class__.__name__)),"w") as f:
            pass
        with open(os.path.join(self.log_folder,"value_history_{}.csv".format(self.algorithm.__class__.__name__)),"w") as f:
            pass
        with open(os.path.join(self.log_folder,"weight_history_{}.csv".format(self.algorithm.__class__.__name__)),"w") as f:
            pass
    def output_results(self):
        '''
        compute various performance measures such as the sharpe ratio.
        '''
        pass