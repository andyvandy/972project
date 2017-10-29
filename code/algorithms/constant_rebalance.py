'''
Constant rebalancing strategy
'''
from .algorithm import *
import numpy as np

class Constant_rebalance(Algorithm):
    def setup(self,first_period):
        self.weight=1.0/self.n_assets # don't want to recompute this all of the time
        weight=self.weight*self.value
        self.portfolio=[weight/price_i for price_i in first_period]

    def step(self,t,history):
        '''
            Look at the most recent period and rebalance accordingly.
            returns a copy of the portfolio so that we can log the results.
        '''
        if self.verbose:
            print(history[t,:])
        self.value=value_portfolio(history[t,:],self.portfolio)

        weight=self.value*self.weight
        self.portfolio= [weight/price_i for price_i in history[t,:]]
        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
