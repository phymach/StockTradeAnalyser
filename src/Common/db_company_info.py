'''
Created on 2014/5/3

@author: phymach
'''

import inspect
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('db_company_info')

class CompanyInfo(db.Model):
    code = db.StringProperty(required=True)
    date_time = db.DateTimeProperty(required=True)
    company_name = db.StringProperty(required=True)

    

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
