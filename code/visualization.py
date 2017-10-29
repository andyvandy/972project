import matplotlib
import matplotlib.pyplot as plt 
import seaborn
import numpy as np
from algorithms.algorithm import value_portfolio

def plot_value_over_time(portfolio_history,market_data):
    #todo make this save the plots
    #just a quick implementation to test things out
    plt.figure()
    time=np.arange(0,market_data.shape[0])
    values= [value_portfolio(portfolio_history[t],market_data[t]) for t in time]
    plt.plot(time,values)
    plt.show()