'''
Created on 2015/1/26

@author: phymach
'''

#############################################################
# Main class of Stock Trade Analyser
# Initial file - Gary - 04/25/2014
# Last modified - Gary - 05/04/2014
#############################################################

import webapp2
import cgi
import logging
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_sys_status
from Common import db_stock_price
from Common import db_company_info
from Common import db_monthly_revenue
from StockInfoLoader import ystockquote
from StockInfoLoader import mopstwse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\main_loader.log')
logger = logging.getLogger('loader')


class LoadMarketPrice(webapp2.RequestHandler):
    
    # GET
    def get(self):
        stock_code = "2330.tw"
        last_update_time = db_sys_status.get_update_time("MarketPrice")
        current_time = datetime.now()

        result = ystockquote.get_historical_prices(stock_code, start_date=datetime.strftime(last_update_time, '%Y%m%d'), end_date=datetime.strftime(current_time, '%Y%m%d'))
        for record in result[1:]:
            db_stock_price.insert_price(code=stock_code,
                                        date_time=datetime.strptime(record[0], '%Y-%m-%d'),
                                        open_price=float(record[1]),
                                        high_price=float(record[2]),
                                        low_price=float(record[3]),
                                        close_price=float(record[4]),
                                        price_change=0.0,
                                        volume=int(record[5]))
            
        db_sys_status.update_module_time("MarketPrice", current_time)
        self.response.write("[%s] Update MarketPrice to database successfully!" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass

class LoadMonthlyRevenue(webapp2.RequestHandler):
    
    # GET
    def get(self):
        stock_type = 'sii'
        last_update_time = db_sys_status.get_update_time("MonthlyRevenue")
        current_time = datetime.now()

        result = mopstwse.get_historical_revenue(stock_type, last_update_time)        
        for i in xrange(len(result.totaldata)):
            company_data = result.totaldata[i]
                
            try:
                db_company_info.insert_info(code=company_data[1], classification=company_data[0], company_name=company_data[2])
                db_monthly_revenue.insert_info(code=company_data[1],
                                            date_time=last_update_time,                                        
                                            month_revenue=int(company_data[3]),
                                            last_month_revenue=int(company_data[4]),
                                            month_revenue_last_year=int(company_data[5]),
                                            percent_month_revenue=company_data[6],
                                            percent_month_revenue_last_year=company_data[7],
                                            month_cumulative_revenue=int(company_data[8]),
                                            month_cumulative_revenue_last_year=int(company_data[9]),
                                            percent_month_cumulative_revenue=company_data[10])
            except:
                print company_data
                raise

        db_sys_status.update_module_time("MonthlyRevenue", current_time)
        self.response.write("[%s] Update MonthlyRevenue to database successfully!" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass
    
class LoadCompanyInfo(webapp2.RequestHandler):
    
    # GET
    def get(self):
        last_update_time = db_sys_status.get_update_time("CompanyInfo")
        current_time = datetime.now()

        db_sys_status.update_module_time("CompanyInfo", current_time)
        self.response.write("[%s] Update CompanyInfo to database successfully!" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass


# loader.load_market_price("2330.tw")
# loader.load_company_info('sii')
app = webapp2.WSGIApplication([('/LoadMarketPrice', LoadMarketPrice)], debug=True)
app = webapp2.WSGIApplication([('/LoadMonthlyRevenue', LoadMonthlyRevenue)], debug=True)
app = webapp2.WSGIApplication([('/LoadCompanyInfo', LoadCompanyInfo)], debug=True)


