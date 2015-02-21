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
from WebComponents import web_index


class FinanceChart(webapp2.RequestHandler):
    
    # GET
    def get(self):
        self.response.write("""<html>
                                    <head>
                                        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
                                        <script type="text/javascript">
                                            google.load("visualization", "1", {packages:["corechart"]});
                                            google.setOnLoadCallback(drawChart);
                                            function drawChart() {
                                                var data = google.visualization.arrayToDataTable([
                                                      ['Mon', 20, 28, 38, 45],
                                                      ['Tue', 31, 38, 55, 66],
                                                      ['Wed', 50, 55, 77, 80],
                                                      ['Thu', 77, 77, 66, 50],
                                                      ['Fri', 68, 66, 22, 15]
                                                      // Treat first row as data as well.
                                                ], true);
                                
                                                var options = { legend:'none'};
                                                var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));
                                                chart.draw(data, options);
                                            }
                                        </script>
                                  </head>
                                  <body>
                                      <div id="chart_div" style="width: 900px; height: 500px;"></div>
                                  </body>
                            </html>""")
        
        
    # POST
    def post(self):
        pass




app = webapp2.WSGIApplication([('/Finance', FinanceChart)], debug=True)


