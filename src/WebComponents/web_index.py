# -*- coding: utf-8 -*-

#############################################################
# Web index
# Initial file - Gary - 05/04/2014
# Last modified - Gary - 05/04/2014
#############################################################


import webapp2
import cgi
from datetime import datetime
from Common import db_stock_price

#def ini(code, date):
#    stockCode = "2330.tw"


# HEADER
def show_header():
    header = "<html>"
    header += "<head>"
    header += "<meta charset='UTF-8>"
    header += "<title>Stock Trade Analyser</title>"
    header += "<script type='text/javascript' src='/WebComponents/jquery-1.11.1.min.js'></script>"
    #herder += "<script language='JavaScript'>"
    #herder += "</script>"
    header += "<link type='text/css' rel='stylesheet' href='/WebComponents/webstyle.css' />"
    header += "</head>"
    header += "<body>"
    return header


# CONTENT
MAIN_PAGE_CONTENT_FORM = """\
    
    <H2>Hello, welcome to StockTradeAnalyser!</H2>
        <form>
          Stock ID:<input value="2330.tw" name="sname">
          , Date:<input type="date" name="sdate" id="sdate" value="2014-01-01">
          , post-type:<input value="web" name="type">
          <input type="submit" value="submit">
        </form>
    
        <!--<a href="http://tw.yahoo.com">Yahoo! TW</a>-->
    """ 

def show_content_form():

    return MAIN_PAGE_CONTENT_FORM
       
def show_content(stockName, selected_date):
    getStockPrice = "<br /> yahoo get_price() sample: [" + stockName + "] $"
    getStockPrice += str( db_stock_price.get_price(stockName, datetime.strptime(selected_date,'%Y-%m-%d')) )

    return getStockPrice


# FOOTER
MAIN_PAGE_FOOTER_TEMPLATE = """\
        <p id='footer_CopyRight'>©2014 All Right Reserved.<p>
      </body>
    </html>
    """
def show_footer():

    return MAIN_PAGE_FOOTER_TEMPLATE
    