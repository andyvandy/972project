'''
Base class that other algorithms will inherit from
'''
import numpy as np

class Algorithm:
    def __init__(self,period,n_assets,verbose=False):
        self.verbose=verbose
        if verbose: "print initializing Algorithm"
        self.period=period
        self.n_assets=n_assets
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