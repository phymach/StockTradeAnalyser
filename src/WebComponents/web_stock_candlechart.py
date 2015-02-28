# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015/2/28

@author: phymach
'''

import webapp2
import cgi
from datetime import datetime
from Common import db_stock_price

# WEB Tabs
from WebComponents import web_news
from WebComponents import web_stock_info
from WebComponents import web_stock_trade_assistant
from WebComponents import web_stock_trade_report
from WebComponents import web_app_info
from WebComponents import web_about
from WebComponents import web_registration
from WebComponents import web_user_profile


# HEADER
def show_header(contents):
    header = """<head>"""
    header += """<script type="text/javascript" src="https://www.google.com/jsapi"></script>"""
    header += """<script type="text/javascript">"""
    header += """    google.load("visualization", "1", {packages:["corechart"]});"""
    header += """    google.setOnLoadCallback(drawChart);"""
    header += """    function drawChart() {"""
    header += """        var data = google.visualization.arrayToDataTable("""
    #contents = [ ['label', low, open, high, close],
    #             ['label', low, open, high, close] ]

    header += contents
    header += """, true);"""
    header += """        var options = { legend:'none'};"""
    header += """        var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));"""
    header += """            chart.draw(data, options);"""
    header += """    }</script>"""
    header += """</head>"""
    
    return header


def show_body():
    body = """<body>"""
    body += """    <div id="chart_div" style="width: 1400px; height: 600px;"></div>"""
    body += web_about.MAIN_PAGE_FOOTER_TEMPLATE
    body += """</body>"""
    return body
       

def show_html(contents):
    html = """<html>"""
    html += show_header(contents)
    html += show_body()
    html += """</html>"""
   
    return html
    
    