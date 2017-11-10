'''
    This is the base class for datafeed objects.
    The key data feeds are:
        -historical
        -live

    The reason for this class is to allow us to use the same infrastructure for back testing as for live trading.
    This is key in the case where we want to use an algo on multiple exchanges

    The format of the data sources should be consistent, 
        -current proposal format:
            -timestamp
            -bid, ask price: (can be set the same if not available)
            -for historical data, each crypto currency should stored in a seperate table 
                and then fed in together when the algo runs rather than compiled into one huge table

    Usage:
        Each datafeed should only be instantiated once under this structure
'''

class DataFeed:


    def __init__(self):
        #store this here so that there is a single source to look to, also makes sense to set it here?
        self.n_assets=None 
        pass

    def get_data(self):
        '''this function is a generator yielding values to the algorithm, 
        in this sense we can control the speed at which we feed in values. 
        This allows us "fastforward" time during the backtest.
        '''
        pass

    def log_data(self):
        '''
        This method is not required but can used to log the data, mostly for live feeds

        '''
        pass



