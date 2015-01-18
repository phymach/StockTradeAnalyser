'''
Created on 2014/5/3

@author: phymach
'''

import os
import inspect
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename='D:\\db_company_info.log')
logger = logging.getLogger('db_company_info')

class CompanyInfo(db.Model):
    code                                = db.StringProperty(required=True)
    date_time                           = db.DateTimeProperty(required=True)
    classification                      = db.StringProperty()                   #���~�O
    company_name                        = db.StringProperty(required=True)
    month_revenue                       = db.IntegerProperty()                  #����禬
    last_month_revenue                  = db.IntegerProperty()                  #�W���禬
    month_revenue_last_year             = db.IntegerProperty()                  #�h�~����禬
    percent_month_revenue               = db.FloatProperty()                    #�W�����W��(%)
    percent_month_revenue_last_year     = db.FloatProperty()                    #�h�~�P��W��(%)
    month_cumulative_revenue            = db.IntegerProperty()                  #���֭p�禬
    month_cumulative_revenue_last_year  = db.IntegerProperty()                  #�h�~�֭p�禬
    percent_month_cumulative_revenue    = db.FloatProperty()                    #�e������W��(%)

def insert_info(code, date_time, company_name):
    s = CompanyInfo(code=code, date_time=date_time, company_name=company_name)
    logger.debug('[%s] Insert record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code, datetime.datetime.strftime(date_time,'%Y/%m/%d')))
    s.put()
    
def get_info(code, date_time):
    q = db.Query(CompanyInfo)
    q.filter('code =', code)
    q.filter('date_time =', date_time)

    result = q.get()
    if result:
        print result.company_name
        return result.company_name
