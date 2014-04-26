'''
Created on 2014/4/18

@author: phymach
'''

import datetime
from google.appengine.ext import db
from google.appengine.api import users


class StockPrice(db.Model):
    code = db.IntegerProperty(required=True)
    date_time = db.DateProperty(required=True)
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
    s.put()
    
def get_price(code, date_time):
    q = db.Query(StockPrice)
    q.filter('code =', code)
    q.filter('date_time =', date_time)
    #q.ancestor(ancestor_key)
    #q.order('-date')
    #for record in q.run(limit=5):
    #    print record.close_price
    result = q.get()
    print result.close_price
    return result.close_price

#class Employee(db.Model):
#    name = db.StringProperty(required=True)
#    role = db.StringProperty(required=True,
#                           choices=set(["executive", "manager", "producer"]))
#    hire_date = db.DateProperty()
#    new_hire_training_completed = db.BooleanProperty(indexed=False)
#    email = db.StringProperty()


# e = Employee(name="John",
#             role="manager",
#             email=users.get_current_user().email())
# e.hire_date = datetime.datetime.now().date()
# e.put()