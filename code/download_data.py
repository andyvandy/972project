'''
Download the data using the ccxt module
USe this file when you want to get new data for back testing

Save the files to seperate csvs so that we don't need to load all of the data in each time.

example usage: 
download_data.py --pairs BTC/USD ETH/USD LTC/USD XRP/USD DASH/USD
'''
import os
import argparse
import ccxt
import time
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Download crypto currency historical data for back testing')
parser.add_argument('--frequency', help='select a frequency for the data. examples: 1m, 5m, 1h,1d',default="1d")
parser.add_argument('--exchange', help='what exchange to use',default='kraken')
parser.add_argument('--start', help='start timestamp. example:"2016-01-01 00:00:00"',default='2016-01-01 00:00:00')
parser.add_argument('--end', help='end timestamp. example:"2016-01-01 00:00:00"',default=None)
parser.add_argument('--pairs', help='pass a list of pairs to download', nargs='+',type=str,default=["BTC/USD BT"])
parser.add_argument('--output', help='folder in which to output data', default=os.path.join("..","data","coins"))

args = parser.parse_args()



hold = 30 # how long to wait on failed request


def main():
    #parse the string and get the class object by name, neat eh?
    exchange = getattr(ccxt, args.exchange)({
    'rateLimit': 3000,
    'enableRateLimit': True,
    # 'verbose': True,
    })

    if args.end==None: args.end = exchange.milliseconds() #set the end to the current time
    else: args.end = exchange.parse8601(args.end)
    arguments={
        "exchange":exchange,
        "from_timestamp":exchange.parse8601(args.start),
        "to_timestamp":args.end,
        "frequency":args.frequency,
        "output_folder":args.output,
    }
    for pair in args.pairs:
        logging.info("downloading data for {}".format(pair))
        download_ohlcv_data(pair=pair,**arguments)


def download_ohlcv_data(exchange,from_timestamp,to_timestamp,pair,output_folder,frequency="1d"):
    
    data=[]

    while from_timestamp < to_timestamp:
        try:
            logging.debug('exchange time {}: Fetching candles starting from {}'.format(exchange.milliseconds(),exchange.iso8601(from_timestamp)))
            ohlcvs =exchange.fetch_ohlcv(pair, frequency, from_timestamp)
            logging.debug("exchange time {}: Fetched {} candles".format(exchange.milliseconds(), len(ohlcvs)))
            if ohlcvs[-1][0] <ohlcvs[0][0]:
                # some exchanges return the results in reverse order! :D
                ohlcvs=ohlcvs[::-1]
            if from_timestamp == ohlcvs[-1][0]:
                # the loop doesn't exit if the end time isn't a multiple of the frequency (notably daily)
                from_timestamp =to_timestamp
            else:
                from_timestamp = ohlcvs[-1][0]
                data += ohlcvs
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            logging.warning('Got an error {} ,retrying in {}'.format(type(error).__name__, error.args,hold))
            time.sleep(hold)

    df=pd.DataFrame(data,
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp']=pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp')
    filename=exchange.id+"_"+pair.replace("/","_")+".csv"
    df.to_csv(os.path.join(output_folder,filename),index=False)
    logging.info("Wrote file: {}".format(filename))

if __name__=="__main__":
    main()