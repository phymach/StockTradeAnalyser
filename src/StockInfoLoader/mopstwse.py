#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
   抓上市與上櫃各股每月營收
   Version : 1.1
   Author : Amin white
   Release Date : 2012-06-27
   Python version : 2.7
'''

import csv, codecs, urllib, datetime, os, time
import logging
from sgmllib import SGMLParser

logger = logging.getLogger(__name__)
    
def get_historical_revenue(stock_type, start_date):
    stock = None
    logger.debug('Get %s market all company revenue data from %s' % (stock_type, datetime.datetime.strftime(start_date, '%Y/%m')))
    #營收網址
    url = "http://mops.twse.com.tw/t21/" + stock_type + "/t21sc03_%s_%s.html" % (start_date.year - 1911, start_date.month)
    #print url
    #解析網頁開始
    webcode = urllib.urlopen(url)
    if webcode.code == 200:
        stock = Parser_htm()
        stock.parse(webcode.read())
    webcode.close()

    return stock
         
#解析營收網頁class
class Parser_htm(SGMLParser):

    #初始化class等同constructor
    def __init__(self):
        SGMLParser.__init__(self)
        
    #初始化變數數值
    def reset(self):
        SGMLParser.reset(self)
        self.isRowData = False
        self.isEmptyData = False
        
        self.isFactoryClass = False
        self.factory_name = ""
        self.isStockId = False
        self.stock_id = ""
        self.isCompanyName = False
        self.nowrapflag = False
        self.nowrapcount = 0
        self.stockdata = []
        self.totaldata = []

    #解析網頁
    def parse(self,data):
        self.feed(data)
        self.close()

    #解析網頁標籤為th的內容
    def start_th(self, attrs):
        #抓取準備解析資料內容起點
        if len(attrs) == 2:
            if attrs[0][0] == 'class' and attrs[0][1] == 'tt' and attrs[1][0] == 'align' and attrs[1][1] == 'left':              
                self.isFactoryClass = True
                self.factory_name = ""        
        #抓取準備解析資料內容終點       
        elif len(attrs) == 4:
            if attrs[0][0] == 'class' and attrs[0][1] == 'tt' and \
               attrs[1][0] == 'nowrap' and attrs[1][1] == 'nowrap' and \
               attrs[2][0] == 'colspan' and attrs[2][1] == '2' and \
               attrs[3][0] == 'align' and attrs[3][1] == 'center':
                self.isRowData = False                

    #解析網頁標籤為tr的內容
    def start_tr(self, attrs):
        if len(attrs) == 1:
            if attrs[0][0] == 'align' and attrs[0][1] == 'right':
                if len(self.stockdata)>0:
                    self.totaldata.append(self.stockdata)
                    self.stockdata = []
                self.isRowData = True

    #解析網頁標籤為td的內容
    def start_td(self, attrs):
        #收尋資料為空字串的起點
        if self.isRowData:
            if len(attrs) == 0:
                self.isEmptyData = True
            #解析td標籤屬性名稱與屬性
            elif len(attrs) == 1:
                if attrs[0][0] == 'align':
                    #抓股票代碼與資料解析起點
                    if attrs[0][1] == 'center':
                        #self.isRowData = True
                        self.isStockId = True
                    #抓公司名稱起點   
                    elif attrs[0][1] == 'left':
                        self.isCompanyName = True       
                #收尋資料為空字串的終點與解析各營收內容起點
                if attrs[0][0] == 'nowrap' and attrs[0][1] == 'nowrap':
                    self.nowrapflag = True
                    self.isEmptyData = False
                    self.nowrapcount += 1

    #取得網頁表格內容是文字,數字以外的資料
    def handle_entityref(self,ref):
        #解析資料內容為空字串
        if self.isEmptyData and ref == 'nbsp':
            self.nowrapcount += 1
            self.stockdata.append("")
            if self.nowrapcount == 8:
                self.isRowData = False
    #開始讀取各公司營收資料到暫存list中
    def handle_data(self, text):
        #產業別
        if self.isFactoryClass:
            self.isFactoryClass = False
            data = unicode(text.strip(), "BIG5").encode('utf8').split('：')
            self.factory_name = unicode(data[1], "utf8")
            logger.debug('產業別 :    %s' % self.factory_name.encode('utf8'))
        elif self.isRowData:
            #公司代碼或稱股票代碼
            if self.isStockId:
                self.isStockId = False
                self.nowrapcount = 0
                logger.debug('公司代號 :    %s' % text.strip())
                self.stock_id = text.strip()
                self.stockdata.append(self.factory_name)
                self.stockdata.append(self.stock_id)
            #公司名稱
            elif self.isCompanyName:
                self.isCompanyName = False
                #使用big5解碼,因為支援字型不夠,就需要加入以下的內容,若使用cp950解碼,只需加入網頁無法呈現的字型即可
                data = text.strip().decode('cp950', 'ignore')
                logger.debug('公司名稱 :    %s' % data.encode('utf8'))
                self.stockdata.append(data)
            elif self.nowrapflag:
                self.nowrapflag = False
                #各營收資料
                if self.nowrapcount == 1:
                    logger.debug('當月營收:    %s'  % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 2:
                    logger.debug('上月營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 3:
                    logger.debug('去年當月營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 4:
                    logger.debug('上月比較增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 5:
                    logger.debug('去年同月增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 6:
                    logger.debug('當月累計營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 7:
                    logger.debug('去年累計營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 8:
                    logger.debug('前期比較增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                    self.isRowData = False

# #函數進入點
# if __name__ == "__main__":
#     main()