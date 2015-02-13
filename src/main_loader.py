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
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_sys_status
from StockInfoLoader import loader

class StockInfoLoad(webapp2.RequestHandler):
    
    # GET
    def get(self):
        last_update_time = db_sys_status.get_update_time("MarketPrice")
        current_time = datetime.now()
        loader.load_market_price("2330.tw", start_date=last_update_time, end_date=current_time)
        db_sys_status.update_module_time("MarketPrice", current_time)
        self.response.write("[%s] Update 2330.tw to database successfully!" % datetime.strftime(current_time, '%m/%d/%Y %I:%M:%S'))
    # POST
    def post(self):
        pass



# loader.load_market_price("2330.tw")
# loader.load_company_info('sii')
app = webapp2.WSGIApplication([('/StockInfoLoader', StockInfoLoad)], debug=True)


