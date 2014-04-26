'''
Created on 2012/11/29

@author: phymach
'''
from datetime import datetime
from StockInfoLoader import ystockquote
from Common import db_stock_price


def load_by_code(stock_code, start_date=datetime(2014, 01, 01)):
    result = ystockquote.get_historical_prices(stock_code, datetime.strftime(start_date, '%Y%m%d'), datetime.strftime(datetime.now(), '%Y%m%d'))
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
        
if __name__=="__main__":
    print load_by_code("2330.tw")