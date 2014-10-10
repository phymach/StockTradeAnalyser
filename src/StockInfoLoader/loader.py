'''
Created on 2012/11/29

@author: phymach
'''
from datetime import datetime
from StockInfoLoader import ystockquote
from Common import db_stock_price


def load_market_price(stock_code, start_date=datetime(2014, 01, 01), end_date=datetime.now()):
    result = ystockquote.get_historical_prices(stock_code, datetime.strftime(start_date, '%Y%m%d'), datetime.strftime(end_date, '%Y%m%d'))
    for record in result[1:]:
        db_stock_price.insert_price(code            = stock_code,
                                    date_time       = datetime.strptime(record[0],'%Y-%m-%d'),
                                    open_price      = float(record[1]),
                                    high_price      = float(record[2]),
                                    low_price       = float(record[3]),
                                    close_price     = float(record[4]),
                                    price_change    = 0.0,
                                    volume          = int(record[5]))
    return result
        
def load_public_info():
    continue
    
if __name__=="__main__":
    print load_market_price("2330.tw")