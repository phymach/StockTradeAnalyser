# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on 05/04/2014

@author: Gary
'''

import webapp2
import cgi
from datetime import datetime
from google.appengine.api import users
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

def login_info():
    # get login
    user = users.get_current_user()
    if user:
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
    else:
        greeting = ('<a href="%s">Sign in or register</a>.' %
                    users.create_login_url('/'))

    return greeting
        

# HEADER
def show_header():
    header =  "<head>"
    header += "<meta charset='UTF-8>"
    header += "<title>Stock Trade Analyser</title>"
    header += "<script type='text/javascript' src='/WebComponents/jquery-1.11.1.min.js'></script>"
    #herder += "<script language='JavaScript'>"
    #herder += "</script>"
    header += "<link type='text/css' rel='stylesheet' href='/WebComponents/webstyle.css' />"
    header += "</head>"
    
    return header


def show_content_form():
    # CONTENT
    MAIN_PAGE_CONTENT_FORM = """\
        
        <div class='style_headline'>Hello, welcome to StockTradeAnalyser!</div>
            <form>
              Stock ID:<input value="2330" name="sname">
              , Date:<input type="date" name="sdate" id="sdate" value="2014-01-01">
              , post-type:<input value="web" name="type">
              <input type="submit" value="submit">
            </form>
        
            <!--<a href="http://tw.yahoo.com">Yahoo! TW</a>-->
        """ 
    return MAIN_PAGE_CONTENT_FORM
       
def show_content(stockName, selected_date):
    selected_date = datetime.strptime(selected_date,'%Y-%m-%d')
    
    price_list = []
    result = db_stock_price.get_price(stockName, selected_date, selected_date)
    if result:
        for record in result:
            price_list.append(str(record.close_price))
            
        getStockPrice = "<br> yahoo get_price() sample: [" + stockName + "] $"
        getStockPrice += ",".join(price_list)
    else:
        getStockPrice = "<br> Can't not find record on selected date!"

    return getStockPrice


def show_body(stockName="", selected_date=""):
    body =  "<body>"
    body += login_info()
    body += "<div>"
    body += "<div class='style_header'>"
    body += "<img src='/WebComponents/logo.png'>"
    body += "<div class='style_menu'>"
    body += "<a href='tw.yahoo.com'> NEWS </a>"
    body += "<a href='www.google.com'> Stock Info </a>"
    body += "<a href=''> Stock Report </a>"
    body += "</div>"
    body += "</div>"
    body += "<div class='style_body'>"
    body += show_content_form()
    
    if selected_date != "":
        body += show_content(stockName, selected_date)
    else:
        body += "wait for input!!"
    
    body += "</div>"
    body += web_about.MAIN_PAGE_FOOTER_TEMPLATE.decode('utf-8')
    body += "</div>"
    body +=  "</body>"
    
    return body


def show_html(stockName="", selected_date=""):
    html = """<html>"""
    html += show_header()
    html += show_body(stockName, selected_date)
    html += """</html>"""
   
    return html
    