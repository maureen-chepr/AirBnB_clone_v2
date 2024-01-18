#!/usr/bin/python3
"""squalchemy DB storage"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import sqlalchemy
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

all_classes = {"User": User, "BaseModel": BaseModel,
                  "Place": Place, "State": State,
                  "City": City, "Amenity": Amenity,
                  "Review": Review}

class DBStorage:
    """class DBstorage that manages storage"""
    __engine = None
    __session = None
    all_classes = ["State", "City", "User", "Place", "Review"]

    def __init__(self):
        """init for database connection"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HBNB_MYSQL_USER,
                                            HBNB_MYSQL_PWD,
                                            HBNB_MYSQL_HOST,
                                            HBNB_MYSQL_DB
                                                )
        self.__engine = create_engine(db, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        if not self.__session:
            self.reload()

        objects = {}
        if isinstance(cls, str):
            cls = all_classes.get(cls, None)

        query_classes = [cls] if cls else all_classes.values()

        for query_cls in query_classes:
            for obj in self.__session.query(query_cls):
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects

        ''' dict_rep = {}
        if cls is None:
            for clas in self.all_classes:
                clas = eval(clas)
                for instance in self.__session.query(clas).all():
                    key = instance.__class__.__name__ + '.' + instance.id
                    dict_rep[key] = instance
        else:
            for instance in self.__session.query(cls).all():
                key = instance.__class__.__name__ + '.' + instance.id
                dict_rep[key] = instance
        return dict_rep
'''
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj in current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self):
        """session closing"""
        self.__session.close()
