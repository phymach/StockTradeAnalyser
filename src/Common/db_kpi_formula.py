'''
Created on 2015/2/2

@author: phymach
'''

import inspect
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import users

logger = logging.getLogger(__name__)

class KPIFormula(db.Model):
    username = db.StringProperty(required=True)
    profile = db.IntegerProperty(required=True)
    kpi_name = db.StringProperty(required=True)
    arg_name = db.StringProperty(required=True)
    arg_value = db.FloatProperty(required=True)
    
