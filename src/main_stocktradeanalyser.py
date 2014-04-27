#############################################################
# Main class of Stock Trade Analyser
# Gary - 04/25/2014 - initial file
#
#############################################################

import webapp2
import cgi
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_stock_price
from StockInfoLoader import ystockquote
from StockInfoLoader import loader

# template test
MAIN_PAGE_FOOTER_TEMPLATE = """\

    <form>Stock ID:
      <input value="" name="sname">, Date:
      <input type="date" name="sdate" id="sdate" value="2014-01-01">
      <input type="submit" value="submit">
    </form>

    <a href="http://tw.yahoo.com">Yahoo! TW</a>

  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):
    
    # GET
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('<html><body>')
        self.response.out.write('Hello, StockTradeAnalyser!')
        
        # set default GOOG      
        if self.request.get('sname') != "":
            stockName = self.request.get('sname')
            selected_date = self.request.get('sdate')

            self.response.out.write('<br /> yahoo get_price() sample: [' + stockName + '] $')
            #self.response.write(ystockquote.get_price(stockName))
            self.response.write(db_stock_price.get_price(stockName, datetime.strptime(selected_date,'%Y-%m-%d')))
        else:
            self.response.write("wait for input!!")
        
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        
    # POST
    def post(self):
        self.request.get('sname')
        self.request.get('sdate')


loader.load_by_code("2330.tw")
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
    