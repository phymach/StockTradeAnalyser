'''
Created on 2012/11/29

@author: phymach
'''
from datetime import datetime
from StockInfoLoader import ystockquote


def load_by_code(stock_code, start_date=datetime(2014, 01, 01)):
    result = ystockquote.get_historical_prices(stock_code, datetime.strftime(start_date, '%Y%m%d'), datetime.strftime(datetime.now(), '%Y%m%d'))
    #for record in result:

    return result
        
if __name__=="__main__":
    print load_by_code("2330.tw")