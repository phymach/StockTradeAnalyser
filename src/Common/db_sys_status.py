'''
Created on 2014/5/3

@author: phymach
'''

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
logger = logging.getLogger('db_sys_status')

class SystemStatus(db.Model):
    module_name = db.StringProperty(required=True)
    last_update_time = db.DateTimeProperty(required=True)    

def update_module_time(module_name, last_update_time=datetime.datetime.now()):
    find = db.Key.from_path('SystemStatus', 'module_name', module_name)
    record = db.get(find)
    if record:
        setattr(record, 'last_update_time', last_update_time)
        record.put()
    else:
        s = SystemStatus(module_name=module_name, last_update_time=last_update_time)
        s.put()
    logger.debug('[%s] Update module: %s last update to: %s.' % (inspect.getframeinfo(inspect.currentframe())[2], module_name, datetime.datetime.strftime(last_update_time,'%Y/%m/%d')))
    
def get_update_time(module_name):
    q = db.Query(SystemStatus)
    q.filter('code =', module_name)
    result = q.get()
    if result:
        print result.last_update_time
        return result.last_update_time
    else:
        return datetime(2014, 01, 01)

