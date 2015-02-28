# -*- coding: utf-8 -*-

#############################################################
# Web index: Index for other pages
# Initial file - Gary - 05/04/2014
# Last modified - Gary - 05/18/2014
#############################################################

#
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
    header += "<body> <div>"
    header += "<div class='style_header'>"
    header += "<img src='/WebComponents/logo.png'>"
    header += "<div class='style_menu'>"
    header += "<a href='tw.yahoo.com'> NEWS </a>"
    header += "<a href='www.google.com'> Stock Info </a>"
    header += "<a href=''> Stock Report </a>"
    header += "</div>"
    header += "</div>"
    header += "<div class='style_body'>"
    return header




def show_content_form():
    # CONTENT
    MAIN_PAGE_CONTENT_FORM = """\
        
        <div class='style_headline'>Hello, welcome to StockTradeAnalyser!</div>
            <form>
              Stock ID:<input value="2330.tw" name="sname">
              , Date:<input type="date" name="sdate" id="sdate" value="2014-01-01">
              , post-type:<input value="web" name="type">
              <input type="submit" value="submit">
            </form>
        
            <!--<a href="http://tw.yahoo.com">Yahoo! TW</a>-->
        """ 
    return MAIN_PAGE_CONTENT_FORM
       
def show_content(stockName, selected_date):
    getStockPrice = "<br /> yahoo get_price() sample: [" + stockName + "] $"
    getStockPrice += str( db_stock_price.get_price(stockName, datetime.strptime(selected_date,'%Y-%m-%d')) )

    return getStockPrice



def show_footer():
    # FOOTER
    MAIN_PAGE_FOOTER_TEMPLATE = """\
            </div>
            <div class="style_footer">
                <div id='footer_CopyRight'>©2014 All Right Reserved.</div>
            </div>
            </div>
          </body>
        </html>
        """
    return MAIN_PAGE_FOOTER_TEMPLATE
    