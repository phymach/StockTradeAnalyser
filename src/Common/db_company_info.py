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

class CompanyInfo(db.Model):
    code                    = db.StringProperty(required=True)      #公司代號
    market_type             = db.StringProperty(required=True)      #產業分類名稱  sii, otc
    classification          = db.StringProperty(required=True)      #產業別
    company_name            = db.StringProperty(required=True)      #公司名稱
    company_address         = db.StringProperty()                   #公司地址
    company_tel             = db.StringProperty()                   #公司電話
    company_open_date       = db.StringProperty()                   #公司成立日
    company_listing_date    = db.StringProperty()                   #公司上市上櫃日
    company_capital         = db.StringProperty()                   #公司資本額

def insert_info(code, market_type, classification, company_name, company_address, company_tel,
                company_open_date, company_listing_date, company_capital):
    s = CompanyInfo(code=code, market_type=market_type, classification=classification,
                    company_name=company_name, company_address=company_address, company_tel=company_tel,
                    company_open_date=company_open_date, company_listing_date=company_listing_date, company_capital=company_capital)
    logger.debug('[%s] Insert record:  code=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code))
    s.put()

def update_info(code, market_type, classification, company_name, company_address, company_tel,
                company_open_date, company_listing_date, company_capital):
    q = db.Query(CompanyInfo)
    q.filter('code =', code)
    result = q.get()
    
    if result:
        logger.debug('[%s] Update record:  code=%s' % (inspect.getframeinfo(inspect.currentframe())[2], code))
        setattr(result, 'market_type', market_type)
        setattr(result, 'classification', classification)
        setattr(result, 'company_name', company_name)
        setattr(result, 'company_address', company_address)
        setattr(result, 'company_tel', company_tel)
        setattr(result, 'company_open_date', company_open_date)
        setattr(result, 'company_listing_date', company_listing_date)
        setattr(result, 'company_capital', company_capital)
        result.put()
    else:
        insert_info(code, market_type, classification, company_name, company_address, company_tel,
                company_open_date, company_listing_date, company_capital)

def get_info(code):
    q = db.Query(CompanyInfo)
    q.filter('code =', code)

    result = q.get()
    if result:
        return result
    
def get_code_list():
    code_list = []
    result = CompanyInfo.all()
    result.order("code")
    
    for i in result:
        code_list.append(i.code)

    return code_list
