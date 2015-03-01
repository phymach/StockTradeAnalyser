#############################################################
# Main class of Stock Trade Analyser
# Initial file - Gary - 04/25/2014
# Last modified - Gary - 05/04/2014
#############################################################

import webapp2
import cgi
import cStringIO
from datetime import datetime
from google.appengine.ext.webapp.util import run_wsgi_app
from Common import db_stock_price
from WebComponents import web_index
from WebComponents import web_stock_candlechart


class MainPage(webapp2.RequestHandler):
    
    # GET
    def get(self):
        if self.request.get('type') == "web":
            stockName = self.request.get('sname')
            selected_date = self.request.get('sdate')
            
            self.response.write(web_index.show_html(stockName, selected_date))
            
        elif self.request.get('type') == "data":
            self.response.write("data")
            
        elif self.request.get('type') == "app":
            self.response.write("app")
        
        elif self.request.get('type') == "candlechart":
            code = self.request.get('code')
            start_date = datetime.strptime(self.request.get('start_date'), "%Y-%m-%d")
            end_date = datetime.strptime(self.request.get('end_date'), "%Y-%m-%d")

            record_text = []
            for record in db_stock_price.get_price(code, start_date=start_date, end_date=end_date):
                record_text.append([record.date_time.strftime("%m/%d"), record.low_price, record.open_price, record.close_price, record.high_price])
            output = cStringIO.StringIO()
            print >>output, record_text
            contents = output.getvalue()
            #print contents
            
            self.response.write(web_stock_candlechart.show_html(contents))
        else:
            self.response.write("Please specify a type!!<br />")
            self.response.write("<form>post-type:<input value='web' name='type'><input type='submit' value='submit'></form>")
        
        
    # POST
    def post(self):
        self.request.get('type')
        self.request.get('sname')
        self.request.get('sdate')




app = webapp2.WSGIApplication([('/', MainPage)], debug=True)


