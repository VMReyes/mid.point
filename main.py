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
                             'logoutlink': users.create_logout_url('/')}
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
        loc2 = float(content_dict['results'][0]['geometry']['location']['lng'])
        loc1 = float(content_dict['results'][0]['geometry']['location']['lat'])
        friends = int(self.request.get('friends'))
        lat=0.00
        lon=0.00
        for i in range(1,friends,1):
            user_query = UserStorage.query(UserStorage.email == self.request.get('femail'+str(i)))
            friend = user_query.get()
            lat += friend.LatLocation
            lon += friend.LongLocation
        lat /= friends + 1
        lon /= friends + 1
        coords = {'lat' : lat,
                  'lon' : lon}

        template = env.get_template('results.html')
        self.response.write(template.render(coords))

class CreateDummies(webapp2.RequestHandler):
    def get(self):
        UserStorage(id = "Prado Inciong", email="prado_jix@yahoo.com", LatLocation = 33.99, LongLocation= -118.47  ).put()
        UserStorage(id = "Jasmine Chau", email="Jasmine_Chau@yahoo.com", LatLocation = 55.0, LongLocation= 118.47  ).put()
        UserStorage(id = "Victor Reyes", email="Victor_Reyes@yahoo.com", LatLocation = -3.99, LongLocation= -118.47  ).put()
        user_query = UserStorage.query()
        users = user_query.fetch()
        self.response.write(users)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')
        if not UserStorage.query(UserStorage.email == user.email()).get():
            UserStorage(email=user.email()).put()
        template_vars = {'name':user.nickname()
        }
        self.response.write(template.render(template_vars))

class ActivitiesHandler(webapp2.RequestHandler):
    def get(self):
        restaurants = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&key=AIzaSyCLQX1qUpEtlls2fjHvThYT7WbufGnOPD0").read()
        restaurants = resturants
        self.response.write("<html>%s</html>" % restaurants)


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers),
    ('/createDummies', CreateDummies),
    ('/login', LoginHandler),
    ('/success', MainPageHandler),
    ('/activities', ActivitiesHandler)
], debug=True)
