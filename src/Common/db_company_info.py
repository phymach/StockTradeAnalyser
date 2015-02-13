#!/usr/bin/python
# -*- coding: utf-8 -*-

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

class CompanyInfo(db.Model):
    code               = db.StringProperty(required=True)      #公司代號
    date_time          = db.DateTimeProperty(required=True)
    market_type        = db.StringProperty()                   # sii, otc
    classification     = db.StringProperty()                   #產業別
    company_name       = db.StringProperty(required=True)      #公司名稱

def insert_info(code, classification, company_name):
    s = CompanyInfo(code=code, classification=classification, company_name=company_name)
    
    logger.debug('[%s] Insert record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code))
    s.put()
    
def get_info(code, date_time):
    q = db.Query(CompanyInfo)
    q.filter('code =', code)

    result = q.get()
    if result:
        print result.company_name
        return result.company_name
