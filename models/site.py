from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from page import Page


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(120), ForeignKey('users.id'))
    pages = relationship("Page", backref=backref('sites'))

    def __init__(self, name=None, owner_id=None):
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return '<Site %r>' % self.name