'''
Created on 2012/11/29

@author: phymach
'''

import logging
import webapp2
from datetime import datetime
from StockInfoLoader import ystockquote
from StockInfoLoader import mopstwse
from Common import db_sys_status
from Common import db_stock_price
from Common import db_company_info

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\loader.log')
logger = logging.getLogger('loader')

class MainPage(webapp2.RequestHandler):
    
    # GET
    def get(self):
        last_update_time = db_sys_status.get_update_time("MarketPrice")
        load_market_price("2330.tw", start_date=last_update_time)
        db_sys_status.update_module_time("MarketPrice", datetime.now())
        self.response.write("[%s] Update 2330.tw to database successfully!" % datetime.strftime(datetime.now(), '%m/%d/%Y %I:%M:%S'))
        
    # POST
    def post(self):
        pass


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
        
        try:
            db_company_info.insert_info(code                                = company_data[1],
                                        date_time                           = start_date,
                                        classification                      = company_data[0],
                                        company_name                        = company_data[2],
                                        month_revenue                       = int(company_data[3]),
                                        last_month_revenue                  = int(company_data[4]),
                                        month_revenue_last_year             = int(company_data[5]),
                                        percent_month_revenue               = company_data[6],
                                        percent_month_revenue_last_year     = company_data[7],
                                        month_cumulative_revenue            = int(company_data[8]),
                                        month_cumulative_revenue_last_year  = int(company_data[9]),
                                        percent_month_cumulative_revenue    = company_data[10])
        except:
            print company_data
            raise

def load_public_info():
    pass
    
if __name__=="__main__":
    pass
#     print load_company_info(stock_type='sii')
#     last_update_time = db_sys_status.get_update_time("MarketPrice")
#     load_market_price("2330.tw", start_date=last_update_time)
#     db_sys_status.update_module_time("MarketPrice", datetime.now())