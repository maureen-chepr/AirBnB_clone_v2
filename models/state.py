#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models.city import City
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade='all, delete-orphan', backref='state')

    else:
        name=""

    if os.getenv('HBNB_TYPE_STORAGE') == 'fs':
        @property
        def cities(self):
            """cities in file storage"""
            result = []
            city_inst = models.storage.all(models.classes['City']).value()
            for k in city_inst:
                if k.state_id == self.id:
                    result.append(k)
            return result
