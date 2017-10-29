import matplotlib
#matplotlib.use('qt5agg')
import matplotlib.pyplot as plt 
import seaborn
import numpy as np
from algorithms.algorithm import value_portfolio

def plot_value_over_time(value_history):
    #todo make this save the plots
    #just a quick implementation to test things out
<<<<<<< HEAD
    plt.figure()
    time=np.arange(0,market_data.shape[0])
    values= [value_portfolio(portfolio_history[t],market_data[t]) for t in time]
    plt.plot(time,values)
=======
    plt.plot(value_history)
>>>>>>> 980256a789d76eae3c8b6ba8ab22005e6e8abde1
    plt.show()