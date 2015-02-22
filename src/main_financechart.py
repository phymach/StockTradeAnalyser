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
from StockInfoLoader import ystockquote
from WebComponents import web_index


class FinanceChart(webapp2.RequestHandler):
    
    # GET
    def get(self):
        record_text = []
        for record in db_stock_price.get_price("1220", start_date=datetime.strptime("2014-12-09", "%Y-%m-%d"), end_date=datetime.strptime("2015-01-01", "%Y-%m-%d")):
            record_text.append([record.date_time.strftime("%m/%d"), record.low_price, record.open_price, record.close_price, record.high_price])
        output = cStringIO.StringIO()
        print >>output, record_text
        contents = output.getvalue()
        print contents
        
        self.response.write("""<html><head>""")
        self.response.write("""<script type="text/javascript" src="https://www.google.com/jsapi"></script>""")
        self.response.write("""<script type="text/javascript">""")
        self.response.write("""    google.load("visualization", "1", {packages:["corechart"]});""")
        self.response.write("""    google.setOnLoadCallback(drawChart);""")
        self.response.write("""    function drawChart() {""")
        self.response.write("""        var data = google.visualization.arrayToDataTable(""")
        #self.response.write("""            [ ['1/1', 20, 28, 38, 45],
        #                                     ['1/2', 31, 38, 55, 66],
        #                                     ['1/3', 50, 55, 77, 80],
        #                                     ['1/4', 77, 77, 66, 50],
        #                                     ['1/5', 68, 66, 22, 15] ]""")
        self.response.write(contents)
        self.response.write(""", true);""")
        self.response.write("""        var options = { legend:'none'};""")
        self.response.write("""        var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));""")
        self.response.write("""            chart.draw(data, options);""")
        self.response.write("""    }</script>""")
        self.response.write("""</head>""")
        self.response.write("""<body>
                                   <div id="chart_div" style="width: 1400px; height: 600px;"></div>
                               </body>""")
        self.response.write("""</html>""")
        
        
    # POST
    def post(self):
        pass




app = webapp2.WSGIApplication([('/Finance', FinanceChart)], debug=True)


