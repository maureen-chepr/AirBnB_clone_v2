#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from models import storage_type
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """intialize state"""
        super().__init__(*args, **kwargs)


        if getenv('HBNB_TYPE_STORAGE') != 'db':
            @property
            def cities(self):
                """Getter attribute for cities in FileStorage"""
                city_list = []
                all_cities = models.storage.all(City)
                for city in all_cities.values():
                    if city.state_id == self.id:
                        city_list.append(city)
                return city_list
