import configparser
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from threading import Lock
import numpy as np


class Model:
    _db_instance = None
    _lock: Lock = Lock()

    """
    Model Class : 
    -use the get_instance method to get an instance of the db
    """

    @classmethod
    def get_instance(cls):
        """
        Configuration method to return db instance
        """
        if cls._db_instance is None:
            with cls._lock:
                if cls._db_instance is None:
                    config = configparser.ConfigParser()
                    config.read("configuration_file.ini")
                    SMART_ELEVATOR_SYSTEM_DB_URI = config.get("CONNECTION_DATA", "SMART_ELEVATOR_SYSTEM_DB_URI")
                    SMART_ELEVATOR_SYSTEM_DB_NAME = config.get("CONNECTION_DATA", "SMART_ELEVATOR_SYSTEM_DB_NAME")

                    cls._db_instance = MongoClient(
                        SMART_ELEVATOR_SYSTEM_DB_URI,
                        maxPoolSize=3,
                        connectTimeoutMS=2500)[SMART_ELEVATOR_SYSTEM_DB_NAME]
        return cls._db_instance

    @classmethod
    def add_user(cls, name: str, face_encoding, floor_number: int):
        """
        Given a name, face_encoding and the floor number, inserts a document with those credentials
        to the `users_info` collection.
        """

        try:
            Model.get_instance().users_info.insert_one({
                "name": name,
                "face_encoding": face_encoding,
                "floor_number": floor_number
            })
            return {"success": True}
        except DuplicateKeyError:
            return {"error": "A user with these information already exists."}

    @classmethod
    def get_all_face_encodings(cls):
        """
        :return: all face encodings in the database
        """
        m_filter = {}
        project = {
            '_id': 0,
            'face_encoding': 1
        }

        result = Model.get_instance().users_info.find(
            filter=m_filter,
            projection=project
        )
        return list(result)

    @classmethod 
    def get_user_info(cls, face_encoding):
        """
        :return: users information with this face_encoding
        """
        
        m_filter = {
            'face_encoding': list(face_encoding)
        }

        project = {}

        result = Model.get_instance().users_info.find(
            filter=m_filter
        )

        return list(result)[0]

