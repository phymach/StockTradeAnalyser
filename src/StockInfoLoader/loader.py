'''
Created on 2012/11/29

@author: phymach
'''

import logging
from datetime import datetime
from StockInfoLoader import ystockquote
from StockInfoLoader import mopstwse
from Common import db_stock_price
from Common import db_company_info

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\loader.log')
logger = logging.getLogger('loader')

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

def load_company_info(stock_type, start_date=datetime(2014, 01, 01)):
    result = mopstwse.get_historical_revenue(stock_type, start_date)
    
    for i in xrange(len(result.totaldata)):
        company_data = result.totaldata[i]

        db_company_info(code                                = company_data[1].encode('utf8'),
                        date_time                           = start_date,
                        classification                      = company_data[0].encode('utf8'),
                        company_name                        = company_data[2].encode('utf8'),
                        month_revenue                       = company_data[3].encode('utf8'),
                        last_month_revenue                  = company_data[4].encode('utf8'),
                        month_revenue_last_year             = company_data[5].encode('utf8'),
                        percent_month_revenue               = company_data[6].encode('utf8'),
                        percent_month_revenue_last_year     = company_data[7].encode('utf8'),
                        month_cumulative_revenue            = company_data[8].encode('utf8'),
                        month_cumulative_revenue_last_year  = company_data[9].encode('utf8'),
                        percent_month_cumulative_revenue    = company_data[10].encode('utf8'))

def load_public_info():
    continue
    
if __name__=="__main__":
    print load_market_price("2330.tw")