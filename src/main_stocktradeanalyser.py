#############################################################
# Main class of Stock Trade Analyser
# Gary - 04/25/2014 - initial file
#
#############################################################

import webapp2
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
#from Common import db_stock_price
from StockInfoLoader import ystockquote

# template test
MAIN_PAGE_FOOTER_TEMPLATE = """\

    <form>Stock ID:
      <input value="" name="sname">
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
        if self.request.get('sname') == "":
            stockName = 'GOOG'
        else:
            stockName = self.request.get('sname')

        self.response.out.write('<br /> yahoo get_price() sample: [' + stockName + '] $')
        self.response.write(ystockquote.get_price(stockName))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        
    # POST
    def post(self):
        self.request.get('sname')


app = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)
