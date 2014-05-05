#############################################################
# Main class of Stock Trade Analyser
# Initial file - Gary - 04/25/2014
# Last modified - Gary - 05/04/2014
#############################################################

import webapp2
import cgi
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_stock_price
from StockInfoLoader import ystockquote
from StockInfoLoader import loader
from WebComponents import web_index


class MainPage(webapp2.RequestHandler):
    
    # GET
    def get(self):

        if self.request.get('type') == "web":
            #self.response.write(web_index.ini(sname, sdate))
            self.response.write(web_index.show_header())
            self.response.write(web_index.show_content_form())
                
            if self.request.get('sname') != "":
                stockName = self.request.get('sname')
                selected_date = self.request.get('sdate')
                self.response.write(web_index.show_content(stockName, selected_date))
                #self.response.out.write('<br /> yahoo get_price() sample: [' + stockName + '] $')
                #self.response.write(ystockquote.get_price(stockName))
                #self.response.write(db_stock_price.get_price(stockName, datetime.strptime(selected_date,'%Y-%m-%d')))
            else:
                self.response.write("wait for input!!")
                
            self.response.write(web_index.show_footer())
            
        elif self.request.get('type') == "data":
            self.response.write("data")
            
        elif self.request.get('type') == "app":
            self.response.write("app")
            
        else:
            self.response.write("Please specify a type!!<br />")
            self.response.write("<form>post-type:<input value='web' name='type'><input type='submit' value='submit'></form>")
        
        
    # POST
    def post(self):
        self.request.get('type')
        self.request.get('sname')
        self.request.get('sdate')



loader.load_by_code("2330.tw")
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
    