import webapp2

import os
import cgi
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class List(db.Model):

    atm_id = db.IntegerProperty(indexed = True)
    e_type = db.StringProperty(indexed = True)
    e_date = db.StringProperty(indexed = True)
    e_time = db.StringProperty(indexed = True)
    f_date = db.StringProperty(indexed = True)
    f_time = db.StringProperty(indexed = True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    def get(self):
        self.render('ebc.html')  
class Signin(MainPage):
    def get(self):
	self.render('signin.html')

    def post(self):
	password = self.request.get("password")
	params = dict(password = password)
	if password == "ebc123" :
	    self.redirect('/errorlist')

        else:
	    params['error_password'] = "invalid password please try again"
	    self.render('signin.html', **params)

class SigninAdmin(MainPage):
    def get(self):
	self.render('adminsignin.html')

    def post(self):
	password = self.request.get("password")
	params = dict(password = password)
	if password == "helpdesk" :
	    self.redirect('/logform.html')

        else:
	    params['error_password'] = "invalid password please try again"
	    self.render('adminsignin.html', **params)

class FrontPage(MainPage):

    def get(self):
	self.render('logform.html')

    def post(self):

	have_error = False
        atm_id = int(self.request.get("atm_id"))
        e_type = self.request.get("e_type")
        e_date = self.request.get("e_date")
        e_time = self.request.get("e_time")
	f_date = self.request.get("f_date")
	f_time = self.request.get("f_time")	
	
        error_list = List(atm_id=atm_id,e_type=e_type,e_date=e_date,e_time=e_time,f_date=f_date,f_time=f_time)
	params = dict(atm_id = atm_id,e_type = e_type)
	if not (atm_id and e_type):
	    params['errorid'] = "you have to insert both ATM-ID and error type"
	    have_error = True
        if have_error:
            self.render('logform.html', **params)    
	else:
	    error_list.put() 			
 	    self.redirect('/errorlist')	   
     	

class ATM_list(Handler):
    
    def get(self):
	errorsss = db.GqlQuery("SELECT * FROM List order by created asc ")
	self.render('ATMs_error.html',errorsss=errorsss)    


	
		
	

app = webapp2.WSGIApplication([('/adminsignin.html',SigninAdmin),('/signin.html',Signin),('/',MainPage),('/logform.html',FrontPage),('/errorlist',ATM_list)], debug=True)
