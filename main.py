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

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())

class ResultsHandlers(webapp2.RequestHandler):
    def get(self):
        loc1 = float(self.request.get('loc1'))
        loc2 = float(self.request.get('loc2'))
        loc3 = float(self.request.get('floc1'))
        loc4 = float(self.request.get('floc2'))
        coords = {'lat' : (loc1 + loc3) / 2,
                  'lon' : (loc2 + loc4) / 2}

        template = env.get_template('results.html')
        self.response.write(template.render(coords))

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/results', ResultsHandlers)
], debug=True)
