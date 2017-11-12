'''
Seperate out the visualizations so that the code doesn't depend on matplotlib

TODO: add saving of figures, and better figures

'''

import matplotlib
#matplotlib.use('qt5agg')
import matplotlib.pyplot as plt 
import seaborn
import numpy as np
import logging
from algorithms.algorithm import value_portfolio

def plot_value_over_time(t,value_history,title="",labels=[]):
    #todo make this save the plots
    #just a quick implementation to test things out

    lineObjects=plt.plot(t,value_history)
    if len(labels): plt.legend(iter(lineObjects),labels)
    plt.title(title)
    plt.show()