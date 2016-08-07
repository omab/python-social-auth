from peewee import *
from datetime import datetime
from flask.ext.login import UserMixin

database_proxy = Proxy()


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database_proxy

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    password = CharField(null=True)
    email = CharField(null=True)
    active = BooleanField(default=True)
    join_date = DateTimeField(default=datetime.now)

    class Meta:
        order_by = ('username',)
