'''
Main file to run all of our code from. Not much to say yet

'''

import argparse
from tqdm import *
from algorithms import online_newton
from algorithms import offline_newton # the base against which we compute regret
from algorithms import constant_rebalance

from visualization import *
from os.path import join
import numpy as np
import pandas as pd

def main(args):
    market_data=pd.read_csv(join("..","data","market_data.csv"),index_col=0, parse_dates=True)
    model_params={
        'eta':0,
        'beta':1,
        'delta':1.0/8,
    }
    sim_params={
        "period":1,
        #"algo_class":constant_rebalance.Constant_rebalance,
        "algo_class":online_newton.Online_newton,
        #"end":market_data.shape[0],
        "end":100,
        "market_data":market_data,
        "verbose":args.verbose,
        "model_params":model_params,
    }
    sim=Simulation(**sim_params)
    sim.run()
    if args.plot: 
        plot_value_over_time(sim.value_history )
        plot_value_over_time(sim.portfolio_history )

class Simulation:
    '''
    General Class meant to simulate all of our algorithms.
    Takes in a pandas dataframe with the historical stock prices
    '''
    def __init__(self,period,algo_class,end,market_data,model_params,verbose=False):
        self.verbose=verbose #for debugging
        self.period=period
        self.end=end
        self.market_data=market_data.as_matrix()
        #self.relative_market_data=market_data.pct_change().fillna(1).as_matrix() +1#extract_relative_prices(self.market_data)
        self.relative_market_data=market_data.pct_change().dropna().as_matrix() +1#extract_relative_prices(self.market_data)
        self.algorithm=algo_class(sim=self,period=period,n_assets=self.market_data.shape[1],verbose=verbose)
        self.model_params=model_params 
        self.p_hist=[]
        self.rel_p_hist=[]
        self.portfolio_history=[] #todo preallocate these
        self.value_history=[]
        

    def run(self):
        '''
        runs the simulation
        if this is slow we can enable storing of the results so that we don't haveto rerun this
        if we avoid printing we can benefit from tqdm's loading bar feature which is quite nice
        '''

        self.algorithm.setup(self.market_data[0,:],model_params=self.model_params)
        self.log_state(0)
        for t in tqdm(range(1,self.end,self.period)):
            self.step(t)


    def step(self,t):
        '''
        Step through one period of the simulation. Add the current most recent price
        Allow the alogorithm to update its portfolio
        assert that the portfolio value doesn't change within a simulation step
        Log the new state
        '''
        if self.verbose:
            print("Simulation step # {}:".format(t))

        self.p_hist= self.market_data[:t+1,:] # we sue these to make sure that we don't accidentally use data we should have access to in our algos
        self.rel_p_hist= self.relative_market_data[:t+1,:]
        initial_value=value_portfolio(self.algorithm.portfolio,self.p_hist[-1])
        #if self.verbose: print(self.price_history)
        self.algorithm.step(t)
        self.log_state(t)
        try:
            assert self.value_history[-1] == initial_value # important to crash if this occurs
        except:
            print("initial value {} -> {} in same step!".format(initial_value, self.value_history[-1]))

    def log_state(self,t):
        self.portfolio_history.append(self.algorithm.portfolio)
        self.value_history.append(value_portfolio(self.market_data[t,:],self.algorithm.portfolio))

    def output_results(self):
        '''
        compute various performance measures such as the sharpe ratio.
        '''
        pass

def extract_relative_prices(market_data):
    return [np.zeros(market_data.shape[1])] +[ np.divide(market_data[i+1],market_data[i]) for i in range(market_data.shape[0]-1)]



if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Run simulations')
    parser.add_argument('--verbose', '-v', action='count',help='use this flag to control debug printouts',default =0)
    parser.add_argument('--plot', '-p', action="store_true",help='turn plotting on')
    args=parser.parse_args()
    main(args)