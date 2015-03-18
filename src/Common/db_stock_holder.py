'''
Created on 2015/2/2

@author: phymach
'''
import os
import inspect
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

logger = logging.getLogger(__name__)

def toInt(val):
    try:
        return(val)
    except ValueError:
        return 0

def toFloat(val):
    try:
        return float(val)
    except ValueError:
        return 0.0

class StockHolder(db.Model):
    code                                = db.StringProperty(required=True)      #公司代號
    date_time                           = db.DateTimeProperty(required=True)


def insert_info(code, date_time, month_revenue):
    s = StockHolder(code=code, date_time=date_time)
    
    logger.debug('[%s] Insert record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code, datetime.datetime.strftime(date_time,'%Y/%m/%d')))
    s.put()
    
    
    
def get_info(code, date_time):
    q = db.Query(StockHolder)
    q.filter('code =', code)
    q.filter('date_time =', date_time)

    result = q.get()
    if result:
        return result