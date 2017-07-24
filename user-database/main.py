from users import UserStorage
import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(_file_)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        UserStorage(id = "Prado Inciong", email="prado_jix@yahoo.com", LatLocation = 33.99, LongLocation= -118.47  ).put()
        UserStorage(id = "Jasmine Chau", email="Jasmine_Chau@yahoo.com", LatLocation = 55.0, LongLocation= 118.47  ).put()
        UserStorage(id = "Victor Reyes", email="Victor_Reyes@yahoo.com", LatLocation = -3.99, LongLocation= -118.47  ).put()
        user_query = UserStorage.query()
        users = user_query.fetch()
        self.response.write(users)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
