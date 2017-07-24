from google.appengine.ext import ndb

class UserStorage(ndb.Model):
    id = ndb.StringProperty()
    email = ndb.StringProperty()
    LatLocation = ndb.FloatProperty()
    LongLocation = ndb.FloatProperty() 
