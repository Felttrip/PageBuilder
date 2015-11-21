from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from models.element_type import ElementType


class Element(Base):
    __tablename__ = 'elements'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('element_types.id'))
    page_id = Column(Integer, ForeignKey('pages.id'))
    order = Column(Integer)
    content = Column(String(256))
    element_type = relationship("ElementType", backref=backref("elements", uselist=False))

    def __init__(self, type_id=None, page_id=None, order=None, content=None):
        self.type_id = type_id
        self.page_id = page_id
        self.order = order
        self.content = content

    def __repr__(self):
        return '<Element %r>' % self.name

    def to_dict(self):
        return {'id': self.id,
                'type_id': self.type_id,
                'page_id': self.page_id,
                'order': self.order,
                'element_type': self.element_type.to_dict()}