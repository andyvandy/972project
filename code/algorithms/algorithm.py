'''
Base class that other algorithms will inherit from
'''
import numpy as np

class Algorithm:
    def __init__(self,period,n_assets):
        self.period=period
        self.n_assets=n_assets
        self.portfolio=[0]*n_assets
        self.value= 100
        self.setup() #implemented in each algo's class

    def value_portfolio(self,prices):
        return np.dot(self.portfolio,prices)

    def step(self,history):
        pass

    def setup(self):
        pass