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
        return self.portfolio

    def step(self,t,history):
        '''
            Look at the most recent period and rebalance accordingly.
            returns a copy of the portfolio so that we can log the results.
        '''
        if self.verbose:
            print(history[t,:])
        value=value_portfolio(np.array(history[t,:]),self.portfolio)

        weight=value*self.weight
        self.portfolio= [weight/price_i for price_i in history[t,:]]
        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(value))
        return self.portfolio
