'''
Main file to run all of our code from. Not much to say yet

TODO:
storing results of a simulation to a file

'''
import logging
logging.basicConfig(level=logging.DEBUG)
import argparse
from tqdm import *
from controller import *
from historical_feed import *
from controller import *
from algorithms import online_newton
from algorithms import offline_newton # the base against which we compute regret
from algorithms import constant_rebalance



from visualization import *
from os.path import join
import numpy as np
import pandas as pd

def main(args):
    data_feed_params={
        "filename":join("..","data",args.data),
        "file_type":"csv",
        "assets":["BTC","LTC","ETH"],#todo add to argparse
        "verbose":args.verbose,
    }
    sim_data_feed=HistoricalFeed(**data_feed_params)

    model_params={
        'eta':0,
        'beta':1,
        'delta':1.0/8,
    }
    controller_params={
        "algo_class":constant_rebalance.Constant_rebalance,
        #"algo_class":online_newton.Online_newton,
        "data_feed":sim_data_feed,
        "verbose":args.verbose,
        "model_params":model_params,
    }
    controller=Controller(**controller_params)
    controller.run()
    if args.plot: 
        plot_value_over_time(controller.value_history )# todo log scale
        plot_value_over_time(controller.portfolio_weight_history ) #todo value weighted not position size weighted.




    


def extract_relative_prices(market_data):
    return [np.zeros(market_data.shape[1])] +[ np.divide(market_data[i+1],market_data[i]) for i in range(market_data.shape[0]-1)]



if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='Run simulations')
    parser.add_argument('--verbose', '-v', action='count',help='use this flag to control debug printouts',default =0)
    parser.add_argument('--plot', '-p', action="store_true",help='turn plotting on')
    parser.add_argument('--data',help='select the data source',default ="coins.csv")
    args=parser.parse_args()
    main(args)