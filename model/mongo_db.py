import configparser
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from threading import Lock


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
        if not cls._db_instance:
            with cls._lock:
                if not cls._db_instance:
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
    def add_user(cls, name, email, hashedpw):
        """
        Given a name, email and password, inserts a document with those credentials
        to the `users` collection.
        """

        """
        Ticket: Durable Writes

        Please increase the durability of this method by using a non-default write
        concern with ``insert_one``.
        """

        try:
            # TODO: User Management
            # Insert a user with the "name", "email", and "password" fields.
            # TODO: Durable Writes
            # Use a more durable Write Concern for this operation.
            Model.get_instance().users.insert_one({
                "name": name,
                "email": email,
                "password": hashedpw
            })
            return {"success": True}
        except DuplicateKeyError:
            return {"error": "A user with the given email already exists."}
