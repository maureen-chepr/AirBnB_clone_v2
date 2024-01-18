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
        cities = relationship("City", backref='state', cascade='all, delete-orphan')

    else:
        name=""

    @property
    def cities(self):
        """returns the list of City instances with
        state_id equals to the current State.id"""
        if getenv("HBNB_TYPE_STORAGE") != "db":
            import models
            from models.city import City
            list_city = []

            cities = models.storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    list_city.append(city)
            return list_city
'''
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """cities in file storage"""
            city_inst = models.storage.all(models.classes['City']).value()
            for k in city_inst:
                if k.state_id == self.id:
                    result.append(k)
            return result
'''
