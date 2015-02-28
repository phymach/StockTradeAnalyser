#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015/1/26

@author: phymach
'''

import webapp2
import cgi
import os, csv, logging, inspect
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_sys_status
from Common import db_stock_price
from Common import db_company_info
from Common import db_monthly_revenue
from StockInfoLoader import ystockquote
from StockInfoLoader import mopstwse
from StockInfoLoader import stockinfotwse

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\main_loader.log')
logger = logging.getLogger('loader')


class LoadMarketPrice(webapp2.RequestHandler):
    
    # GET
    def get(self):
        last_update_time = db_sys_status.get_update_time("StockPrice")
        current_time = datetime.now()
            
        for stock_code in db_company_info.get_code_list():
            tw_stock_code = stock_code + ".tw"
            
            result = ystockquote.get_historical_prices(tw_stock_code, start_date=datetime.strftime(last_update_time, '%Y%m%d'), end_date=datetime.strftime(current_time, '%Y%m%d'))
            for record in result[1:]:
                db_stock_price.update_price(code=stock_code,
                                            date_time=datetime.strptime(record[0], '%Y-%m-%d'),
                                            open_price=float(record[1]),
                                            high_price=float(record[2]),
                                            low_price=float(record[3]),
                                            close_price=float(record[4]),
                                            price_change=0.0,
                                            volume=int(record[5]))
                logger.debug("Insert record date=%s, code=%s into db_stock_price" % (datetime.strptime(record[0], '%Y-%m-%d'), stock_code))
                
            db_sys_status.update_module_time("StockPrice", current_time)
        self.response.write("[%s] Update MarketPrice to database successfully!<br>" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
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
                #db_company_info.insert_info(code=company_data[1], classification=company_data[0], company_name=company_data[2])
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
        self.response.write("[%s] Update MonthlyRevenue to database successfully!<br>" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass
    
class LoadCompanyInfo(webapp2.RequestHandler):
    folder_path = os.path.dirname(inspect.getfile(inspect.currentframe()))
    
    # GET
    def get(self):
        last_update_time = db_sys_status.get_update_time("CompanyInfo")
        current_time = datetime.now()

        market_type = ["sii", "otc"]
        with open(os.path.join(self.folder_path, "StockInfoLoader", "stock_type_list.csv")) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for i in xrange(len(market_type)):
                    result = stockinfotwse.get_info(market_type[i], row['no'])
                    for j in xrange(len(result)):
                        info = result[j]
                        
                        db_company_info.update_info(code=info.code, market_type=market_type[i], 
                                                    classification=row['class'].decode('utf8'),
                                                    company_name=info.company_name.decode('utf8'),
                                                    company_address=info.company_address.decode('utf8'),
                                                    company_tel=info.company_tel.decode('utf8'),
                                                    company_open_date=info.company_open_date.decode('utf8'),
                                                    company_listing_date=info.company_listing_date.decode('utf8'),
                                                    company_capital=info.company_capital.decode('utf8'))
                        logger.debug("Insert data %s:%s into db_company_info" % (market_type[i], info.code))
            
        db_sys_status.update_module_time("CompanyInfo", current_time)
        self.response.write("[%s] Update CompanyInfo to database successfully!<br>" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass


# loader.load_market_price("2330.tw")
# loader.load_company_info('sii')

app = webapp2.WSGIApplication([('/LoadMonthlyRevenue', LoadMonthlyRevenue),
                               ('/LoadCompanyInfo', LoadCompanyInfo),
                               ('/LoadMarketPrice', LoadMarketPrice)], debug=True)

