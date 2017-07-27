import webapp2
import jinja2
from users import *
from google.appengine.api import users
import urllib2
import json
import itertools


env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env.globals.update(zip=zip)



class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        user = users.get_current_user()
        if user:
            template_vars = {'logstatus':"Log Out",
                             'logoutlink': users.create_logout_url('/')
                             }
            if UserStorage.query(UserStorage.email == user.email()).get().setup==True:
                template_vars['address'] = UserStorage.query(UserStorage.email == user.email()).get().address
            self.response.write(template.render(template_vars))
        else:
            template_vars = {'logstatus': "Log In",
                             'logoutlink': users.create_login_url('/login')}
            self.response.write(template.render(template_vars))

    def post(self):
        user = users.get_current_user()
        person = UserStorage.query(UserStorage.email == users.get_current_user().email()).get()
        person.id = self.request.get('name')
        address = self.request.get('user_LatLocation')
        person.address = address
        address = address.replace(" ", "+")
        content = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyADJhWkgPHBu3SXXrtqnJNmdmz7Xu_mhRc" % address).read()
        content_dict = json.loads(content)
        person.LatLocation = float(content_dict['results'][0]['geometry']['location']['lat'])
        person.LongLocation = float(content_dict['results'][0]['geometry']['location']['lng'])
        person.setup = True
        person.put()
        template = env.get_template('index.html')
        if user:
            template_vars = {'logstatus':"Log Out",
                             'logoutlink': users.create_logout_url('/'),
                             'address':person.address}
            self.response.write(template.render(template_vars))
        else:
            template_vars = {'logstatus': "Log In",
                             'logoutlink': users.create_login_url('/login')}
            self.response.write(template.render(template_vars))


class ResultsHandlers(webapp2.RequestHandler):
    def get(self):
        address = str(self.request.get('loc1'))
        address = address.replace(" ", "+")
        content = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyADJhWkgPHBu3SXXrtqnJNmdmz7Xu_mhRc" % address).read()
        content_dict = json.loads(content)
        lng = float(content_dict['results'][0]['geometry']['location']['lng'])
        lat = float(content_dict['results'][0]['geometry']['location']['lat'])

        friends = int(self.request.get('friends'))
        template_vars = {'location_list': [],
                         'names': [],
                         'ratings':[],
                         'price_ranges':[]
                         }
        template_vars['location_list'].append({'lat':lat,'long':lng})
        for i in range(1,friends+1,1):
            user_query = UserStorage.query(UserStorage.email == self.request.get('femail'+str(i)))
            print user_query
            friend = user_query.get()
            template_vars['location_list'].append({'lat':friend.LatLocation,'long':friend.LongLocation})
            lat += friend.LatLocation
            lng += friend.LongLocation
        lat /= (float(friends) + 1)
        lng /= (float(friends) + 1)
        template_vars['lat'] = lat
        template_vars['lon'] = lng

        coordsquery = str(lat) + "," + str(lng)
        restaurants = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=3000&type=restaurant&key=AIzaSyADJhWkgPHBu3SXXrtqnJNmdmz7Xu_mhRc" % coordsquery)
        restaurants = json.load(restaurants)
        restaurants = restaurants['results']
        for i in range(0,5,1):
            print restaurants[i]['name'].encode('utf-8')
            template_vars['names'].append(restaurants[i]['name'])
            if 'rating' in restaurants[i]:
                c = restaurants[i]['rating']
                a = "%1.2f" % restaurants[i]['rating']
            template_vars['ratings'].append(a)
        template = env.get_template('results.html')
        self.response.write(template.render(template_vars))


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')
        template_vars = {'name':user.nickname(),
                         'autofill1': "",
                         'autofill2': ""}
        found_user = UserStorage.query(UserStorage.email == user.email()).get()
        if found_user:
            template_vars['autofill1'] = found_user.id
            template_vars['autofill2'] = found_user.address
        else:
            useremail=user.email()
            useremail=useremail.lower()
            print useremail
            UserStorage(email=useremail).put()

        self.response.write(template.render(template_vars))

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about_us.html')
        self.response.write(template.render())

class ContactUs(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('contact_us.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers),
    ('/login', LoginHandler),
    ('/success', MainPageHandler),
    ('/AboutUs', AboutUs),
    ('/ContactUs',ContactUs),
], debug=False)
