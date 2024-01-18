#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
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
        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            self.updated_at = \
                datetime.strptime(kwargs.get('updated_at',
                                             datetime.now().isoformat()),
                                  '%Y-%m-%dT%H:%M:%S.%f').isoformat()
            self.created_at = \
                datetime.strptime(kwargs.get('created_at',
                                             datetime.now().isoformat()),
                                  '%Y-%m-%dT%H:%M:%S.%f').isoformat()

            kwargs.pop('_class_', None)

            for key, value in kwargs.items():
                setattr(self, key, str(value))

        '''if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
                if "__class__" not in key:
                    setattr(self, key, value)
        else:
            # from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()'''

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        # from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.pop("_sa_instance_state")
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
