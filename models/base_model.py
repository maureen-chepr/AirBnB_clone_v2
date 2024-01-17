#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import os
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime,
                            default=datetime.utcnow(),
                            nullable=False
                            )
        updated_at = Column(DateTime,
                            default=datetime.utcnow(),
                            nullable=False
                            )
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            self.updated_at = datetime.strptime(kwargs.get('updated_at',\
                                            datetime.now().isoformat()),
                                            '%Y-%m-%dT%H:%M:%S.%f')
            self.created_at = datetime.strptime(kwargs.get('created_at',\
                                            datetime.now().isoformat()),
                                            '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            for key, value in kwargs.items():
                # key = key.replace("_", " ")
                if not hasattr(self, key):
                    setattr(self, key, str(value))
            # self.__dict__.update(kwargs)
        
        #if kwargs:
            #for key, val in kwargs.items():
                #if key in ("created_at", "updated_at"):
                    #val = datetime.strptime(kwargs['updated_at'],
                    #                        '%Y-%m-%dT%H:%M:%S.%f')
                #if "__class__" not in key:
                    #setattr(self, key, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dicto = self.__dict__.copy()
        if "created_at" in dicto:
            dicto["created_at"] = dicto["created_at"].strftime(time)
        if "updated_at" in dicto:
            dicto["updated_at"] = dicto["updated_at"].strftime(time)
        dicto["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in dicto:
            del dicto["_sa_instance_state"]
        return dicto

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
