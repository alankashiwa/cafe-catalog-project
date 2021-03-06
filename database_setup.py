from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    email = Column(String(50), nullable = False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    items = relationship('Item', cascade="all, delete-orphan")

    @property
    def serialize(self):
        """ """
        return {
            'id': self.id,
            'name': self.name,
            'Item': [i.serialize for i in self.items],
        }

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    image_url = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ """
        return {
            'cat_id': self.category_id,
            'description': self.description,
            'id': self.id,
            'title': self.name,
            'price': self.price,
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
