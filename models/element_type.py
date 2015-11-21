from sqlalchemy import Column, Integer, String
from database import Base


class ElementType(Base):
    __tablename__ = 'element_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(256))


    def __repr__(self):
        return '<Element Type %r, description: %r>' % self.name % self.description

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description}
