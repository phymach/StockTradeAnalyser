import re, ystockquote, codecs
import dictToObj
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('StockPortfolio')

class StockPortfolio(object):
    dict_stock_id = {}
    
    def __init__(self):
        self.dict_stock_id = self.getStockList()

    def getStockInfo(self, strStockId):
        return ystockquote.get_all('%s.TW' % strStockId)
        
    def getStockList(self):
        f = codecs.open('stock_id_list.txt', encoding='utf-8', mode='r')
        text= f.read()
        f.close()
        dict_stock_id={}
        for stock in re.findall('\d{4}\t[\S ]+', text):
            stock_id,stock_name = stock.split('\t',1)
            dict_stock_id[stock_id] = stock_name
        return dict_stock_id

    def priceBelow(self, floatPrice):
        for stock_id in self.dict_stock_id.keys():
            stock_price = eval(ystockquote.get_price('%s.TW' % stock_id))
            if stock_price==0.0 or stock_price>floatPrice:
                del self.dict_stock_id[stock_id]

    def dividendAbove(self, floatDividend):
        for stock_id in self.dict_stock_id.keys():
            stock_dividend = eval(ystockquote.get_dividend_per_share('%s.TW' % stock_id))
            if stock_dividend<floatDividend:
                del self.dict_stock_id[stock_id]
    
    def near52WeekLow(self, floatPercentage):
        # floatPercentage = (Price -L) / (H-L)
        for stock_id in self.dict_stock_id.keys():
            stock_price = eval(ystockquote.get_price('%s.TW' % stock_id))
            stock_high = eval(ystockquote.get_52_week_high('%s.TW' % stock_id))
            stock_low = eval(ystockquote.get_52_week_high('%s.TW' % stock_id))
            if (stock_price - stock_low) > (stock_high-stock_low)*floatPercentage:
                del self.dict_stock_id[stock_id]

    def savePortfolio(self):
        f = codecs.open('portfolio_list.txt', encoding='utf-8', mode='w')
        for k in self.dict_stock_id.keys():
            f.writelines('%s %s\n' % (k,self.dict_stock_id[k]))
        f.close()

def checkStockExists(stock_info):
    return True if not str(stock_info['stock_exchange'])=='"N/A"' else False



if __name__=="__main__":
    portfolio = StockPortfolio()
    portfolio.priceBelow(20.0)
    portfolio.dividendAbove(1.0)
    portfolio.near52WeekLow(10.0)
    for stock_id in sorted(portfolio.dict_stock_id.keys()):
        print stock_id, portfolio.dict_stock_id[stock_id]
        logger.debug('%s %s:  %s' % (stock_id, portfolio.dict_stock_id[stock_id], str(portfolio.getStockInfo(stock_id))))
    portfolio.savePortfolio()