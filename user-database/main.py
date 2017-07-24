from users import UserStorage
import jinja2
import webapp2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('user_templates'))

class UserHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('user.html')
        self.response.out.write(main_template.render())

    def post(self):
        user_name = self.request.get("user_name")
        user_email = self.request.get("email")
        user_LatLocation = float(self.request.get("user_LatLocation"))
        user_LongLocation = float(self.request.get("user_LongLocation"))
        UserStorage(id = user_name, email=user_email, LatLocation = user_LatLocation, LongLocation= user_LongLocation ).put()

        user_query = UserStorage.query()
        users = user_query.fetch()
        #self.response.write(users)



app = webapp2.WSGIApplication([
    ('/', UserHandler)
], debug=True)
