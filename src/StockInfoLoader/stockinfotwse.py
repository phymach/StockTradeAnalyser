#!/usr/bin/env python
# -*- coding: utf-8 -*-
    
#---------------------------------------------
#   抓上市與上櫃各股相關資料
#   Version : 1.1
#   Author : Amin white
#   Release Date : 2012-01-01
#   Python version : 2.7.2
#---------------------------------------------
    
import urllib, logging
from sgmllib import SGMLParser

logger = logging.getLogger(__name__)

def get_info(market_type, class_no):
    company_list = []

    #個股票網址
    url = "http://mops.twse.com.tw/mops/web/ajax_t51sb01?step=1&firstin=1&TYPEK=%s&code=%s" % (market_type, class_no)
    #解析網頁開始
    webcode = urllib.urlopen(url)

    if webcode.code == 200:
        stock = ParseWebData()
        stock.parse(webcode.read())
        webcode.close()
        stock.close()
         
        if stock.webexist:
            logger.info(market_type + " " + class_no + " web parser OK......")
            
            for j in range(0, len(stock.stockid)):
                company_info = CompanyInfo()
                company_info.code                   = stock.stockid[j]
                company_info.company_name           = stock.stockcompanyname[j]
                company_info.company_address        = stock.stockcompanyaddress[j]
                company_info.company_tel            = stock.stockcompanytel[j]
                company_info.company_open_date      = stock.stockcompanyopendate[j]
                company_info.company_listing_date   = stock.stockcompanylistingdate[j]
                company_info.company_capital        = stock.stockcompanycapital[j]
                
                #company_info.print_info()
                company_list.append(company_info)
        else:
            logger.warning( market_type + " " + class_no + " not exist......")

    return company_list

class CompanyInfo():
    def __init__(self):
        self.code                   = ""
        self.classification         = ""
        self.company_name           = ""
        self.company_address        = ""
        self.company_tel            = ""
        self.company_open_date      = ""
        self.company_listing_date   = ""
        self.company_capital        = ""
        
    def print_info(self):
        print self.code + ", " + self.classification + ", " + self.company_name + ", " + self.company_address + ", " + self.company_tel + ", " + self.company_open_date + ", " + self.company_listing_date + ", " + self.company_capital


class ParseWebData(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)

    def reset(self):
        SGMLParser.reset(self)
        self.webexist = False
        self.nowrapflag = False
        self.styleflag = False
        self.nowrapcount = 0
        self.stylecount = 0
        self.stockcompanyname = []
        self.stockcompanyaddress = []
        self.stockcompanytel = []
        self.stockcompanyopendate = []
        self.stockcompanylistingdate = []
        self.stockcompanycapital = []
        self.stockid = []

    def parse(self,data):
        self.feed(data)
        self.close()
 
    def start_table(self, attrs):
        if attrs[0][0] == 'class' and attrs[0][1] == 'noBorder':
            self.webexist = True                 

    def start_tr(self, attrs):
        self.nowrapflag = False
        self.nowrapcount = 0
        self.styleflag = False
        self.stylecount = 0

    def start_td(self, attrs):
        for name, value in attrs:
            if len(attrs) == 1:
                if name == 'nowrap':
                    self.nowrapflag = True
                    self.nowrapcount += 1                       
                
            elif len(attrs) == 2:
                #print len(attrs)
                if name == 'style':
                    if value == 'text-align:left !important;' or value == 'text-align:right !important;':
                        self.styleflag = True
                        self.stylecount += 1                  

    def handle_data(self, text):

        if self.nowrapflag :
            if self.nowrapcount == 1:
                self.stockid.append(text)
                #print "stockid : " + text
                self.nowrapflag = False
            elif self.nowrapcount == 7:
                self.stockcompanyopendate.append(text)
                #print "opendate : " + text
                self.nowrapflag = False
            elif self.nowrapcount == 8:
                self.stockcompanylistingdate.append(text)
                #print "listingdate : " + text
                self.nowrapflag = False

        if self.styleflag :
            if self.stylecount == 1:
                self.stockcompanyname.append(text)
                #print "name : " + text
                self.styleflag = False
            elif self.stylecount == 2:
                self.stockcompanyaddress.append(text)
                #print "address : " + text
                self.styleflag = False
            elif self.stylecount == 4:
                self.stockcompanytel.append(text)
                #print "tel : " + text
                self.styleflag = False
            elif self.stylecount == 5:
                self.stockcompanycapital.append(text.strip().replace(",", ""))
                #print "capital : " + text.strip().replace(",", "")
                self.styleflag = False 

if __name__ == "__main__":
    get_info()
