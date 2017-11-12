'''
Online newton strategy

A form of follow the leader optimization

TODO:
    -when the trading frequency is lower than the data frequency should we still calculate values?

'''

import numpy as np 
import pandas as pd 
from .algorithm import *
from scipy.optimize import minimize


class Online_newton(Algorithm):
    def setup(self,intial_portfolio,initial_period,model_params):
        self.portfolio=intial_portfolio
        self.eta=model_params['eta']
        self.beta=model_params['beta']
        self.delta=model_params['delta']
        self.trade_frequency=model_params['trade_frequency']
        self.previous_closes=self.format_market_data(initial_period)

        #store the reusable part of computing A and b
        self.a_summation=0
        self.b_summation=0

    def format_market_data(self,market_data):
        '''
        Basically throw away anything that isn't the closing price
        Expecting data to come in as a tuple of the timestamp and a 2d data frame where the dimensions are assets and attributes
        TODO: maybe roll this into the algorithm base class?
        '''
        return market_data.loc[:,'close']


    def step(self,t,market_data):
        '''
            
        '''
        if self.last_trade != None and (t-self.last_trade).days < self.trade_frequency:
            # we need to wait longer until rebalancing
            return 

        #calculate the values that are pertinent from the market data
        closing_prices= self.format_market_data(market_data)
        returns=closing_prices/self.previous_closes 
        self.value=value_portfolio(closing_prices,self.portfolio)




        if self.verbose >1 :
            print("prices:",closing_prices )
            print("portfolio:",self.portfolio )
            print("value:",self.value )

        #we compute the summation terms like this so that we can maintain O(t) run time
        self.a_summation+= -1.0/np.dot(self.portfolio,returns)**2 * np.outer(returns,returns)
        self.b_summation+= 1.0/np.dot(self.portfolio,returns) *returns

        A_t_m1=self.a_summation + np.identity(len(self.portfolio))
        b_t_m1=(1+1.0/self.beta)*self.b_summation 
        if self.verbose >1 : 
            print("A_t_m1:\n {}".format(A_t_m1))
            print("b_t_m1:",b_t_m1)
        A_t_m1_inv= np.linalg.inv(A_t_m1)
        if self.verbose >1 : print(A_t_m1_inv)

        newton_portfolio=projection_in_norm(q=self.delta*A_t_m1_inv @ np.array(b_t_m1),A=A_t_m1,cur_p=self.portfolio,prices=closing_prices,verbose=self.verbose)

        if self.eta== 0:
            self.portfolio=newton_portfolio
        else:
            uniform_portfolio=  self.value/closing_prices/closing_prices.shape[0]
            raise NotImplementedError

        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
            print("\tnew value: {}".format(value_portfolio(closing_prices,self.portfolio) ))

        #update values, doing this here so that early exit doesn't result in inconsistent updating
        #maybe this should be a function
        self.previous_closes=closing_prices



def projection_in_norm(q,A,cur_p,prices,verbose=0):
    value=value_portfolio(prices,cur_p)
    bounds=[(0,upper_bound) for upper_bound in value/prices[1:]]
    
    cons = ({'type': 'ineq', 'fun': lambda x:  value-value_portfolio(prices[1:],x) })
    value=value_portfolio(prices,cur_p)
    if verbose>1:
        print("initial value =",value)
    def target_function(x):
        p=np.concatenate(([1-sum(x)],x))
        #print("p,q:",p,q)
        return (q-p) @ A @ np.transpose(q-p) 

    res= minimize(target_function,cur_p[1:],bounds=bounds,constraints=cons)
    new_port=np.concatenate(([1-sum(res.x)],res.x))
    new_port=[new_port[i]*value/prices[i] for i in range(len(prices))]

    if verbose >1 : print(res)
    if verbose >1 : print(new_port)
    if verbose>1: print("new value =",value_portfolio(prices,new_port))
    return new_port#