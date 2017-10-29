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
    sim_params={
        "period":1,
        "algo_class":constant_rebalance.Constant_rebalance,
        "end":market_data.shape[0],
        "market_data":market_data,
        "verbose":args.verbose,
    }
    sim=Simulation(**sim_params)
    sim.run()
    plot_value_over_time(sim.value_history)
    plot_value_over_time(sim.market_data)

class Simulation:
    '''
    General Class meant to simulate all of our algorithms.
    Takes in a pandas dataframe with the historical stock prices
    '''
    def __init__(self,period,algo_class,end,market_data,verbose=False):
        self.verbose=verbose #for debugging
        self.period=period
        self.end=end
        self.market_data=market_data.as_matrix()
        self.algorithm=algo_class(period=period,n_assets=self.market_data.shape[1],verbose=verbose) 
        self.price_history=[]
        self.portfolio_history=[] #todo preallocate these
        self.value_history=[]

    def run(self):
        '''
        runs the simulation
        if this is slow we can enable storing of the results so that we don't haveto rerun this
        if we avoid printing we can benefit from tqdm's loading bar feature which is quite nice
        '''

<<<<<<< HEAD
        self.portfolio_history.append(self.algorithm.setup(self.market_data[0,:]))
        for t in range(1,self.end,self.period):

        self.algorithm.setup(self.market_data[0,:])
        self.log_state(0)
        for t in tqdm(range(1,self.end,self.period)):

=======
        self.algorithm.setup(self.market_data[0,:])
        self.log_state(0)
        for t in tqdm(range(1,self.end,self.period)):
>>>>>>> cbd909a370f5181ba885b924a19c7055a496cb3e
            self.step(t)


    def step(self,t):
        '''
        Step through one period of the simulation. Add the current most recent price
        Allow the alogorithm to update its portfolio
        Log the new state
        '''
        if self.verbose:
            print("Simulation step # {}:".format(t))
        self.price_history= self.market_data[:t+1,:]
        #if self.verbose: print(self.price_history)
        self.algorithm.step(t,self.price_history)
        self.log_state(t)

    def log_state(self,t):
        self.portfolio_history.append(self.algorithm.portfolio)
        self.value_history.append(value_portfolio(self.market_data[t,:],self.algorithm.portfolio))

    def output_results(self):
        '''
        compute various performance measures such as the sharpe ratio.
        '''
        pass

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Run simulations')
    parser.add_argument('--verbose', '-v', action='count',help='use this flag to control debug printouts')
    args=parser.parse_args()
    main(args)