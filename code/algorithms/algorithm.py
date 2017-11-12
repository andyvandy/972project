'''
Base class that other algorithms will inherit from

The algorithm is responsible for setting the portfolio vector each period

Initially I had this setup where the algorithm could access the simulation object it lived in and its attributes , 
I think that this bi directional access of data is just asking for trouble.  
'''
import numpy as np

class Algorithm:
    def __init__(self,n_assets,verbose=False):
        self.verbose=verbose
        if verbose: print(" initializing Algorithm")
        self.n_assets=n_assets #todo remove
        self.last_trade=None

    

    def step(self,history):
        pass

    def setup(self):
        pass

def value_portfolio(prices,portfolio):
    #maybe not the right place for this function
    return np.dot(prices,portfolio)