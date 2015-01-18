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

class CompanyInfo(db.Model):
    code                                = db.StringProperty(required=True)      #公司代號
    date_time                           = db.DateTimeProperty(required=True)
    classification                      = db.StringProperty()                   #產業別
    company_name                        = db.StringProperty(required=True)      #公司名稱
    month_revenue                       = db.IntegerProperty()                  #當月營收
    last_month_revenue                  = db.IntegerProperty()                  #上月營收
    month_revenue_last_year             = db.IntegerProperty()                  #去年當月營收
    percent_month_revenue               = db.FloatProperty()                    #上月比較增減(%)
    percent_month_revenue_last_year     = db.FloatProperty()                    #去年同月增減(%)
    month_cumulative_revenue            = db.IntegerProperty()                  #當月累計營收
    month_cumulative_revenue_last_year  = db.IntegerProperty()                  #去年累計營收
    percent_month_cumulative_revenue    = db.FloatProperty()                    #前期比較增減(%)

def insert_info(code, date_time, classification, company_name, month_revenue, last_month_revenue, month_revenue_last_year, percent_month_revenue, percent_month_revenue_last_year,
                month_cumulative_revenue, month_cumulative_revenue_last_year, percent_month_cumulative_revenue):
    s = CompanyInfo(code=code, date_time=date_time, classification=classification, company_name=company_name, 
                    month_revenue=month_revenue, last_month_revenue=last_month_revenue, month_revenue_last_year=month_revenue_last_year,
                    percent_month_revenue=percent_month_revenue, percent_month_revenue_last_year=percent_month_revenue_last_year,
                    month_cumulative_revenue=month_cumulative_revenue, month_cumulative_revenue_last_year=month_cumulative_revenue_last_year, percent_month_cumulative_revenue=percent_month_cumulative_revenue)
    
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
