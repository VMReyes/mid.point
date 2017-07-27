# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
from users import *
from google.appengine.api import users
import urllib2
import json

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


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
                             'logoutlink': users.create_logout_url('/')}
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
                         'names': []
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
        print template_vars
        template_vars['lat'] = lat
        template_vars['lon'] = lng

        coordsquery = str(lat) + "," + str(lng)
        print coordsquery
        restaurants = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=500&type=restaurant&key=AIzaSyADJhWkgPHBu3SXXrtqnJNmdmz7Xu_mhRc" % coordsquery)
        restaurants = json.load(restaurants)
        restaurants = restaurants['results']
        for i in range(0,5,1):
            template_vars['names'].append(restaurants[i]['name'])
        print template_vars['names'][0]
        template = env.get_template('results.html')
        self.response.write(template.render(template_vars))


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')
        UserStorage(email=user.email()).put()
        template_vars = {'name':user.nickname()}
        
        template_vars['autofill1'] = UserStorage.query(UserStorage.email == user.email()).get().id
        template_vars['autofill2'] = UserStorage.query(UserStorage.email == user.email()).get().address
        self.response.write(template.render(template_vars))

class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about_us.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers),
    ('/login', LoginHandler),
    ('/success', MainPageHandler),
    ('/AboutUs', AboutUs),
], debug=True)
