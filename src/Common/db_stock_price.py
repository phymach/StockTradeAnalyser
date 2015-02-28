'''
Created on 2014/4/18

@author: phymach
'''

import inspect
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
logger = logging.getLogger('db_stock_price')

class StockPrice(db.Model):
    code = db.StringProperty(required=True)
    date_time = db.DateTimeProperty(required=True)
    open_price = db.FloatProperty()
    high_price = db.FloatProperty()
    low_price = db.FloatProperty()
    close_price = db.FloatProperty(required=True)
    price_change = db.FloatProperty()
    volume = db.IntegerProperty()
    

def insert_price(code, date_time, open_price, high_price, low_price, close_price, price_change, volume):
    s = StockPrice(code=code, date_time=date_time, open_price=open_price,
               high_price=high_price, low_price=low_price, close_price=close_price,
               price_change=price_change, volume=volume)
    logger.debug('[%s] Insert record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code, datetime.datetime.strftime(date_time,'%Y/%m/%d')))
    s.put()

def update_price(code, date_time, open_price, high_price, low_price, close_price, price_change, volume):
    q = db.Query(StockPrice)
    q.filter('code =', code)
    q.filter('date_time =', date_time)
    result = q.get()
    
    if result:
        logger.debug('[%s] Update record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code, datetime.datetime.strftime(date_time,'%Y/%m/%d')))
        setattr(result, 'open_price', open_price)
        setattr(result, 'high_price', high_price)
        setattr(result, 'low_price', low_price)
        setattr(result, 'close_price', close_price)
        setattr(result, 'price_change', price_change)
        setattr(result, 'volume', volume)
        result.put()
    else:
        insert_price(code, date_time, open_price, high_price, low_price, close_price, price_change, volume)
        
    
def get_price(code, start_date, end_date=datetime.datetime.now()):
    q = db.Query(StockPrice)
    q.filter('code =', code)
    q.filter('date_time >=', start_date)
    q.filter('date_time <=', end_date)
    #q.ancestor(ancestor_key)
    #q.order('-date')
    #for record in q.run(limit=5):
    #    print record.close_price
    result = q.fetch(limit=None)
    if result:
        return result
