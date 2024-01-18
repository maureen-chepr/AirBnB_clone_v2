#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review
from models.review import Review


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        reviews = relationship('Review',
                               cascade='all,delete-orphan',
                               backref='user')
        places = relationship('Place', backref='user', cascade='all, delete-orphan')

    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
