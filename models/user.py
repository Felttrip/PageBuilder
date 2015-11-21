from sqlalchemy import Column, String, select
from sqlalchemy.orm import relationship, backref
from database import Base
from site import Site

class User(Base):

    __tablename__ = 'users'
    id = Column(String(120), primary_key=True)
    name = Column(String(50))
    api_key = Column(String(120))
    access_token = Column(String(120))
    sites = relationship("Site", backref=backref('users'))

    def __init__(self, id=None, name=None, api_key=None, access_token=None):
        self.name = name
        self.id = id
        self.api_key = api_key
        self.access_token = access_token

    def __repr__(self):
        return '<User %r>' % self.name

