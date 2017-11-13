'''
Main file to run all of our code from. Not much to say yet

TODO:
storing results of a backtest to a file
Split up the backtest,paper,and live modes more
loading of algorithms modules by name
setting of logging level from args

'''
import logging
logging.basicConfig(level=logging.DEBUG)
import argparse
from tqdm import *
from controller import *
from historical_feed import *
from live_feed import *
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
        "pairs":args.pairs,
        "exchange":args.exchange,
    }
    model_params={}
    controller_params={
        "log_folder":args.logfolder,
    }


    if args.mode==0: #backtest
        data_feed_params.update({
            "verbose":args.verbose,
            "folder":join("..","data",args.data),
        })
        controller_data_feed=HistoricalFeed(**data_feed_params)
    elif args.mode==1 or args.mode==2:
        logging.info("configuring for live data feed")
        data_feed_params.update({
            "frequency":"1m",
        })
        model_params.update({"data_column":"last"})
        controller_params.update({"price_column_name":"last"})
        controller_data_feed=LiveFeed(**data_feed_params)
    model_params.update({
        'eta':0,
        'beta':1.0,
        'delta':1.0/8,
        'trade_frequency': 5 ,#in days
    })
    controller_params.update({
        "algo_class":constant_rebalance.Constant_rebalance,
        #"algo_class":online_newton.Online_newton,
        "data_feed":controller_data_feed,
        "verbose":args.verbose,
        "model_params":model_params,
    })
    controller=Controller(**controller_params)
    controller.run()
    if args.plot: 
        plot_value_over_time(controller.timestamps,controller.value_history ,title="Portfolio value using {}".format(args.algo) )# todo log scale
        plot_value_over_time(controller.timestamps,controller.portfolio_weight_history,title="Portfolio value weights under {}".format(args.algo),labels=controller.asset_names ) #todo value weighted not position size weighted.




    


def extract_relative_prices(market_data):
    return [np.zeros(market_data.shape[1])] +[ np.divide(market_data[i+1],market_data[i]) for i in range(market_data.shape[0]-1)]



if __name__ =="__main__":
    #todo some of these should be in a config file instead of being arguments... it's starting to get crowded
    parser = argparse.ArgumentParser(description='Run simulations')
    parser.add_argument('--verbose', '-v', action='count',help='use this flag to control debug printouts',default =0)
    parser.add_argument('--plot', '-p', action="store_true",help='turn plotting on')
    parser.add_argument('--data',help='select the data source folder',default =os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"data","coins"))
    parser.add_argument('--exchange',help="what exchange to use", default = "kraken") #todo make multi exchange algos work
    parser.add_argument('--pairs', help='pass a list of pairs to download', nargs='+',type=str,default=["BTC/USD","ETH/USD","LTC/USD","XRP/USD"])
    parser.add_argument('--algo', help='The algo you want to use in the algos folder',default="Online_newton")
    parser.add_argument('--mode', help='backtest|paper|live',type=int,default=0)
    parser.add_argument('--logfolder', help='set this option if you want to log controller logs to a folder',type=str,default=None) 
    args=parser.parse_args()
    main(args)