'''
Created on 2012/11/29

@author: phymach
'''


# The ystockquote module provides a Python API for retrieving stock data from Yahoo Finance.

# Sample Usage:
import ystockquote
print ystockquote.get_price('2498.TW')
#529.46
stock_info =  ystockquote.get_all('000.TW')
#{'stock_exchange': '"NasdaqNM"', 'market_cap': '268.6B', '200day_moving_avg': '29.2879', 
#'52_week_high': '31.84', 'price_earnings_growth_ratio': '1.45', 'price_sales_ratio': '5.33', 
#'price': '28.65', 'earnings_per_share': '1.423', '50day_moving_avg': '28.7981', 
#'avg_daily_volume': '55579700', 'volume': '25330856', '52_week_low': '26.48', 'short_ratio': '1.60', 
#'price_earnings_ratio': '28.65', 'dividend_yield': '1.38', 'dividend_per_share': '0.40', 
#'price_book_ratio': '8.76', 'ebitda': '20.441B', 'change': '-0.39', 'book_value': '3.315'}


print str(stock_info['stock_exchange'])

