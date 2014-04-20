import webapp2
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


app = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)
