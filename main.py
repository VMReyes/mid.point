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

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())

class ResultsHandlers(webapp2.RequestHandler):
    def get(self):
        loc1 = float(self.request.get('loc1'))
        loc2 = float(self.request.get('loc2'))
        for key, value in self.request.get():
            print(key, value)
            print(key)
        user_query = UserStorage.query(UserStorage.email == self.request.get('femail1'))
        friend = user_query.get()
        coords = {'lat' : (loc1 + friend.LatLocation) / 2,
                  'lon' : (loc2 + friend.LongLocation) / 2}

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

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers),
    ('/createDummies', CreateDummies)
], debug=True)
