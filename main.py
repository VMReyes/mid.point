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


env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())

class ResultsHandlers(webapp2.RequestHandler):
    def get(self):
        loc1 = float(self.request.get('loc1'))
        loc2 = float(self.request.get('loc2'))
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

        if user:
            if UserStorage.query(UserStorage.email==user.nickname(), UserStorage.setup == True).get():
                template_vars = {'name': user.nickname(),
                                 'logout_url': users.create_logout_url('/')}
                self.response.write(template.render(template_vars))
            else:
                template_vars = {'name': user.nickname(),
                                 'logout_url': users.create_logout_url('/')}
                self.response.write(template.render(template_vars))
        else:
            self.response.write('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/login'))


class SuccessHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        user_LatLocation = float(self.request.get('user_LatLocation'))
        user_LongLocation = float(self.request.get('user_LongLocation'))
        UserStorage(email=users.get_current_user().email(),id=name,LatLocation=user_LatLocation,LongLocation=user_LongLocation,setup=True).put()


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers),
    ('/createDummies', CreateDummies),
    ('/login', LoginHandler),
    ('/success', SuccessHandler)
], debug=True)
