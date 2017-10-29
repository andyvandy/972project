import matplotlib
#matplotlib.use('qt5agg')
import matplotlib.pyplot as plt 
import seaborn
import numpy as np
from algorithms.algorithm import value_portfolio

def plot_value_over_time(value_history):
    #todo make this save the plots
    #just a quick implementation to test things out
    plt.plot(value_history)
    plt.show()