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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\mopstwse.log')
logger = logging.getLogger('mopstwse')
    
# def main():
#     #上市櫃公司自90年6月才有登入月營收資料
# 
#     #包含上市與上櫃
#     stockkind = ['sii', 'otc']
# 
#     #指定儲存的路徑,可自行修改儲存路徑
#     Savefiledir = 'D:\\Revenue\\'    
# 
#     #建立儲存營收CSV資料夾
#     if not os.path.isdir(Savefiledir):
#         os.makedirs(Savefiledir)
# 
#     #取得使用當天的日期
#     today = datetime.datetime.today()
#     todaysec = time.mktime(datetime.datetime(int(today.strftime('%Y')), int(today.strftime('%m')), int(today.strftime('%d'))).timetuple())
# 
#     for i in xrange(len(stockkind)):
#         stocktype = stockkind[i]
#         for j in range(2012, 2013):
#             pyADYear = str(j)
#             pyROCYear = str(j - 1911)
#             for k in range(1, 13):
# 
#                 #取得從1月至今日每月的營收
#                 Revenuedaysec = time.mktime(datetime.datetime(j, k, 10).timetuple())
#                 if Revenuedaysec <= todaysec:
# 
#                     print '取得 ' + pyADYear + ' 年 ' + str('%02d' %k) + ' 月 ' + stocktype + ' 全部公司營收資料' 
#                     #營收網址
#                     url = "http://mops.twse.com.tw/t21/" + stocktype + "/t21sc03_" + pyROCYear + "_" + str(k) + ".html"
# 
#                     #解析網頁開始
#                     webcode = urllib.urlopen(url)
#                     if webcode.code == 200:
#                         stock = Parser_htm()
#                         stock.parse(webcode.read())
#                         webcode.close()
# 
#                     #儲存CSV檔名
#                     SaveCSVname = Savefiledir + stocktype + '_' + pyADYear + str('%02d' %k) + '.csv'
#                     print '設定寫入檔案名稱與格式內容......'
# 
#                     #開始寫入檔案準備
#                     fileoption = codecs.open(SaveCSVname, 'wb')
# 
#                     #指定檔案以UTF8儲存
#                     fileoption.write(codecs.BOM_UTF8)
# 
#                     #指定CSV檔分隔的方式
#                     writer = csv.writer(fileoption, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
# 
#                     print '寫入營收至 ' + SaveCSVname +  ' 開始......'
#                     #寫入欄位說明
#                     writer.writerow([u'產業別'.encode('utf8'), u'公司代號'.encode('utf8'), u'公司名稱'.encode('utf8'), u'當月營收'.encode('utf8'), u'上月營收'.encode('utf8'),\
#                                      u'去年當月營收'.encode('utf8'), u'上月比較增減(%)'.encode('utf8'), u'去年同月增減(%)'.encode('utf8'), u'當月累計營收'.encode('utf8'), \
#                                      u'去年累計營收'.encode('utf8'), u'前期比較增減(%)'.encode('utf8')])
# 
#                     for i in xrange(len(stock.totaldata)):
#                         totaldata = stock.totaldata[i]
# 
#                         #寫入每間公司各營收資料
#                         writer.writerow([totaldata[0].encode('utf8'), totaldata[1].encode('utf8'), totaldata[2].encode('utf8'), \
#                                          totaldata[3].encode('utf8'), totaldata[4].encode('utf8'), totaldata[5].encode('utf8'), \
#                                          totaldata[6].encode('utf8'), totaldata[7].encode('utf8'), totaldata[8].encode('utf8'), \
#                                          totaldata[9].encode('utf8'), totaldata[10].encode('utf8')])
#                     #關閉檔案
#                     fileoption.close()                    
#                     print '寫入營收至 ' + SaveCSVname + ' 完成......\n'


def get_historical_revenue(stock_type, start_date):
    stock = None
    logger.debug('取得 %s %s全部公司營收資料' % (datetime.datetime.strftime(start_date, '%Y/%m'), stock_type))
    #營收網址
    url = "http://mops.twse.com.tw/t21/" + stock_type + "/t21sc03_%s_%s.html" % (start_date.year - 1911, start_date.month)
    print url
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
        self.bPrintDetail = True
        self.bStartParserHeml = False
        self.bStartParserdata = False
        self.bDataempty = False
        
        self.bItemclass = False
        self.szitemclass = ""
        self.bStockid = False
        self.szstockid = ""
        self.bCompanyname = False
        self.nowrapflag = False
        self.nowrapcount = 0
        self.stockdata = []
        self.totaldata = []

    #解析網頁
    def parse(self,data):
        self.feed(data)
        self.close()

    #解析網頁標籤為tr的內容
    def start_tr(self, attrs):
        if len(attrs) == 1:
            if attrs[0][0] == 'align':
                if attrs[0][1] == 'right':
                    self.bStartParserdata = True

    #解析網頁標籤為th的內容
    def start_th(self, attrs):
        #抓取準備解析資料內容起點
        if len(attrs) == 2:
            if attrs[0][0] == 'class' and attrs[0][1] == 'tt' and attrs[1][0] == 'align' and attrs[1][1] == 'left':              
                self.bItemclass = True
                self.szitemclass = ""
                self.bStartParserHeml = True
                
        #抓取準備解析資料內容終點       
        if len(attrs) == 4:
            if attrs[0][0] == 'class' and attrs[0][1] == 'tt' and \
               attrs[1][0] == 'nowrap' and attrs[1][1] == 'nowrap' and \
               attrs[2][0] == 'colspan' and attrs[2][1] == '2' and \
               attrs[3][0] == 'align' and attrs[3][1] == 'center':
                self.bStartParserHeml = False
                self.bStartParserdata = False                

    #解析網頁標籤為td的內容
    def start_td(self, attrs):
        #解析td標籤屬性名稱與屬性
        if len(attrs) == 1:
            if attrs[0][0] == 'align':
                
                #抓股票代碼與資料解析起點
                if attrs[0][1] == 'center':
                    self.bStartParserdata = True
                    self.bStockid = True
                    
                #抓公司名稱起點   
                if attrs[0][1] == 'left':
                    self.bCompanyname = True
                    
            #收尋資料為空字串的終點與解析各營收內容起點
            if attrs[0][0] == 'nowrap' and attrs[0][1] == 'nowrap':
                self.nowrapflag = True
                self.bDataempty = False
                self.nowrapcount += 1                

        #收尋資料為空字串的起點
        if len(attrs) == 0:
            self.bDataempty = True

    #取得網頁表格內容是文字,數字以外的資料
    def handle_entityref(self,ref):
        #解析資料內容為空字串
        if ref == 'nbsp':
            if self.bDataempty:
                self.stockdata.append("")
                self.nowrapcount += 1
                #print ref + " " + str(self.nowrapcount)
            
    #開始讀取各公司營收資料到暫存list中
    def handle_data(self, text):
        #產業別
        if self.bItemclass:
            data = unicode(text.strip(), "BIG5").encode('utf8').split('：')
            self.szitemclass = unicode(data[1], "utf8")
            if self.bPrintDetail:
                logger.debug('產業別 :    %s' % self.szitemclass.encode('utf8'))
            self.bItemclass = False
               
        if self.bStartParserdata:
            #公司代碼或稱股票代碼
            if self.bStockid :
                if self.bPrintDetail:
                    logger.debug('公司代號 :    %s' % text.strip())
                self.szstockid = text.strip()
                self.stockdata.append(self.szitemclass)
                self.stockdata.append(self.szstockid)
                self.bStockid = False
                self.nowrapcount = 0

            #公司名稱
            if self.bCompanyname :
                #使用big5解碼,因為支援字型不夠,就需要加入以下的內容,若使用cp950解碼,只需加入網頁無法呈現的字型即可
                data = text.strip().decode('cp950', 'ignore')
                if self.bPrintDetail:
                    logger.debug('公司名稱 :    %s' % data.encode('utf8'))
                self.stockdata.append(data)
                self.bCompanyname = False            

            if self.nowrapflag :
                self.nowrapflag = False
                #各營收資料
                if self.nowrapcount == 1:
                    if self.bPrintDetail:
                        logger.debug('當月營收:    %s'  % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 2:
                    if self.bPrintDetail:
                        logger.debug('上月營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 3:
                    if self.bPrintDetail:
                        logger.debug('去年當月營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 4:
                    if self.bPrintDetail:
                        logger.debug('上月比較增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 5:
                    if self.bPrintDetail:
                        logger.debug('去年同月增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 6:
                    if self.bPrintDetail:
                        logger.debug('當月累計營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 7:
                    if self.bPrintDetail:
                        logger.debug('去年累計營收 :    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                elif self.nowrapcount == 8:
                    if self.bPrintDetail:
                        logger.debug('前期比較增減(%%):    %s' % text.strip())
                    data = text.strip().replace(",", "")
                    self.stockdata.append(data)
                    self.totaldata.append(self.stockdata)
                    self.stockdata = []

# #函數進入點
# if __name__ == "__main__":
#     main()