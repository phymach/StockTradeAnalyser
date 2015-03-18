#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

class MonthRevenue(db.Model):
    code                                = db.StringProperty(required=True)      #���q�N��
    date_time                           = db.DateTimeProperty(required=True)
    month_revenue                       = db.IntegerProperty()                  #����禬
    last_month_revenue                  = db.IntegerProperty()                  #�W���禬
    month_revenue_last_year             = db.IntegerProperty()                  #�h�~����禬
    percent_month_revenue               = db.FloatProperty()                    #�W����W��(%)
    percent_month_revenue_last_year     = db.FloatProperty()                    #�h�~�P��W��(%)
    month_cumulative_revenue            = db.IntegerProperty()                  #���֭p�禬
    month_cumulative_revenue_last_year  = db.IntegerProperty()                  #�h�~�֭p�禬
    percent_month_cumulative_revenue    = db.FloatProperty()                    #�e�����W��(%)

def insert_info(code, date_time, month_revenue, last_month_revenue, month_revenue_last_year, percent_month_revenue, percent_month_revenue_last_year,
                month_cumulative_revenue, month_cumulative_revenue_last_year, percent_month_cumulative_revenue):
    s = MonthRevenue(code=code, date_time=date_time,
                    month_revenue=month_revenue,
                    last_month_revenue=last_month_revenue,
                    month_revenue_last_year=month_revenue_last_year,
                    percent_month_revenue=toFloat(percent_month_revenue),
                    percent_month_revenue_last_year=toFloat(percent_month_revenue_last_year),
                    month_cumulative_revenue=month_cumulative_revenue,
                    month_cumulative_revenue_last_year=month_cumulative_revenue_last_year,
                    percent_month_cumulative_revenue=toFloat(percent_month_cumulative_revenue))
    
    logger.debug('[%s] Insert record:  code=%s, date_time=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code, datetime.datetime.strftime(date_time,'%Y/%m/%d')))
    s.put()
    
    
    
def get_info(code, date_time):
    q = db.Query(MonthRevenue)
    q.filter('code =', code)
    q.filter('date_time =', date_time)

    result = q.get()
    if result:
        return result