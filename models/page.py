from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from element import Element

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    site_id = Column(Integer, ForeignKey('sites.id'))
    order = Column(Integer)
    elements = relationship("Element", backref=backref('pages'))

    def __init__(self, name=None, site_id=None, order=None):
        self.name = name
        self.site_id = site_id
        self.order = order

    def __repr__(self):
        return '<Page %r>' % self.name

    def to_dict(self):
        res = {'id':self.id,
                'name': self.name,
                'site_id':self.site_id,
                'order':self.order,
                'elements': []}
        for els in self.elements:
            res['elements'].append(els.to_dict())
        return res