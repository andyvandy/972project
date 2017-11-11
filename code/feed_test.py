import os
import pandas
from data_feed import *
from historical_feed import *

DATA_DIR=os.path.join("..","data")
COINS=['bch','btc','eth']
def load_coin_csvs_to_pandas():
    coin_dfs=[pd.read_csv(os.path.join(DATA_DIR,coin+".csv"), index_col=0, parse_dates=True)['price(USD)'] for coin in COINS]

    output_df=pd.concat(coin_dfs,axis=1).dropna()
    output_df.columns=COINS

    output_df.index = output_df.index.strftime("%Y-%m-%d 23:59:59") #convert to end of day timestamps
    return output_df

def test_historical_feed_sqlite():
    '''
    we are testing that the coin db that is loaded sql is the same as the one we get from the CSVs/ that it works
    '''
    hist_feed=HistoricalFeed(os.path.join(DATA_DIR,"test_coins.db"),file_type="sqlite")
    verification_df=load_coin_csvs_to_pandas()
    assert (verification_df == hist_feed.df).all().all()

def test_historical_feed_csv():
    '''
    we are testing that the coin csv that is loaded sql is the same as the one we get from the CSVs/ that it works
    '''
    hist_feed=HistoricalFeed(os.path.join(DATA_DIR,"coins.csv"),file_type="csv")
    #verification_df=load_coin_csv_to_pandas()
    #assert (verification_df == hist_feed.df).all().all()
hist_feed=HistoricalFeed(os.path.join(DATA_DIR,"coins.csv"),file_type="csv",assets=["ETH","BTC","LTC"])
i=0
print(hist_feed.df.columns.tolist())

#for row in hist_feed.get_data():
#    i+=1
#    if i>10:
#        sys.exit()
#    print(row)
#    print(row[1].loc[:,'close'])
#    print(row[1].loc[:,'close'].shape)
#    print(row[1].loc[:,'close'].sum()/row[1].loc[:,'close'])
#    #print(row[1].loc[(slice("ETH","BTC","LTC"),slice('close'))])