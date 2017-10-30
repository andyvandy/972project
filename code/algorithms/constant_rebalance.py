'''
Constant rebalancing strategy
'''
from .algorithm import *
import numpy as np

class Constant_rebalance(Algorithm):
    def setup(self,first_period,model_params):
        weight=self.uniform_weight*self.value
        self.portfolio=[weight/price_i for price_i in first_period]

    def step(self,t):
        '''
            Look at the most recent period and rebalance accordingly.
        '''
        if self.verbose:
            print(history[t,:])
        self.value=value_portfolio(self.sim.p_hist[t,:],self.portfolio)

        weight=self.value*self.uniform_weight
        self.portfolio= [weight/price_i for price_i in self.sim.p_hist[t,:]]
        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
