'''
Online newton strategy
first period is the uniform portfolio

'''

import numpy as np 
import pandas as pd 
from .algorithm import *
from scipy.optimize import minimize
# Load Testing Data 

# ibm_df = pd.read_csv('IBM.csv')
# coca_df = pd.read_csv('KO.csv')

class Online_newton(Algorithm):
    def setup(self,first_period,model_params):
        self.eta=model_params['eta']
        self.beta=model_params['beta']
        self.delta=model_params['delta']
        
        weight=self.uniform_weight*self.value
        self.portfolio=[weight/price_i for price_i in first_period]

    def step(self,t):
        '''
            
        '''
        
        self.value=value_portfolio(self.sim.p_hist[t,:],self.portfolio)
        p_norm=[self.sim.p_hist[t,i]*self.portfolio[i]/self.value for i in range(len(self.portfolio)) ]
        if self.verbose >1 :
            print("prices:",self.sim.p_hist[t,:] )
            print("portfolio:",self.portfolio )
            print("value:",self.value )
            print("norm portfolio:",p_norm )
            print("norm val:",value_portfolio(self.sim.p_hist[t,:],p_norm) )
        #uniform portion 

        weight=self.value*self.uniform_weight
        uniform_portfolio= [weight/price_i for price_i in self.sim.p_hist[t,:]]

        if t<5:
            self.portfolio=uniform_portfolio
            return
        #other portion

        A_t_m1=np.sum([
                    (1.0/(np.dot(self.sim.rel_p_hist[i,:],p_norm)**2)) * np.outer(self.sim.rel_p_hist[i,:],self.sim.rel_p_hist[i,:])
                    for i in range(t)
                    ],axis=0)+np.identity(self.n_assets)
        if self.verbose >1 : print("A_t_m1:\n {}".format(A_t_m1))
        A_t_m1_inv= np.linalg.inv(A_t_m1)
        if self.verbose >1 : print(A_t_m1_inv)
        b_t_m1=(1.0+1.0/self.beta)*np.sum([
                                    (1.0/np.dot(self.sim.rel_p_hist[i,:],p_norm)) *(self.sim.rel_p_hist[i,:])
                                    for i in range(t)] ,axis=0
                                    )
        if self.verbose >1 : print("b_t_m1",b_t_m1)
        if self.verbose >1 : 
            for i in range(t):
                print((1.0/np.dot(self.sim.rel_p_hist[i,:],p_norm)) *(self.sim.rel_p_hist[i,:]))
                print((self.sim.rel_p_hist[i,:]),(1.0/np.dot(self.sim.rel_p_hist[i,:],p_norm)))
        newton_portfolio=projection_in_norm(q=self.delta*A_t_m1_inv @ b_t_m1,A=A_t_m1,cur_p=self.portfolio,prices=self.sim.p_hist[t,:],verbose=self.verbose)

        #newton_portfolio=[new_pnorm[i]/self.sim.p_hist[t,i]* self.value for i in range(len(new_pnorm)) ] 
        if self.eta== 0:
            self.portfolio=newton_portfolio
        else:
            raise NotImplementedError

        if self.verbose:
            print("\tportfolio: {}".format(self.portfolio))
            print("\tvalue: {}".format(self.value))
            print("\tnew value: {}".format(value_portfolio(self.sim.p_hist[t,:],self.portfolio) ))
            #print([np.transpose(self.sim.rel_p_hist[i,:]) for i in range(t)])
            #print(np.outer(self.sim.rel_p_hist[t-1,:], self.sim.rel_p_hist[t-1,:].T)  )




#def projection_in_norm(q,A,cur_p,prices,verbose=0):
#    bounds=[(0,None)] *(len(cur_p)-1)
#    cons = ({'type': 'ineq', 'fun': lambda x:  -value_portfolio(prices[1:],x)+value })
#    value=value_portfolio(prices,cur_p)
#    if verbose>1:
#        print("initial value =",value)
#    def target_function(x):
#        p=np.concatenate(([(value-value_portfolio(prices[1:],x))/prices[0]],x))
#        print("p,q:",p,q)
#        return (q-p) @ A @ np.transpose(q-p) 
#
#    res= minimize(target_function,cur_p[1:],bounds=bounds,constraints=cons)
#    new_port=np.concatenate(([(value-value_portfolio(prices[1:],res.x))/prices[0]],res.x))
#
#    if verbose >1 : print(res)
#    if verbose >1 : print(new_port)
#    if verbose>1: print("new value =",value_portfolio(prices,new_port))
#    return new_port#

def projection_in_norm(q,A,cur_p,prices,verbose=0):
    bounds=[(0,None)] *(len(cur_p)-1)
    cons = ({'type': 'ineq', 'fun': lambda x:  -sum(x)+1 })
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