'''
Base class that other algorithms will inherit from

The algorithm is responsible for setting the portfolio vector each period
'''
import numpy as np

class Algorithm:
    def __init__(self,sim,period,n_assets,verbose=False):
        self.verbose=verbose
        if verbose: "print initializing Algorithm"
        self.sim=sim
        self.period=period
        self.n_assets=n_assets
        self.uniform_weight=1.0/self.n_assets # don't want to recompute this all of the time
        self.portfolio=[0]*n_assets
        self.value= 100
         #implemented in each algo's class

    

    def step(self,history):
        pass

    def setup(self):
        pass

def value_portfolio(prices,portfolio):
    #maybe not the right place for this function
    return np.dot(prices,portfolio)