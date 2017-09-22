from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    image_url = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """ """
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
