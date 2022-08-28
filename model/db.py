import configparser

from pymongo import MongoClient


def get_db():
    """
    Configuration method to return db instance
    """
    config = configparser.ConfigParser()
    config.read("configuration_file.ini")
    SMART_ELEVATOR_SYSTEM_DB_URI = config.get("CONNECTION_DATA", "SMART_ELEVATOR_SYSTEM_DB_URI")
    SMART_ELEVATOR_SYSTEM_DB_NAME = config.get("CONNECTION_DATA", "SMART_ELEVATOR_SYSTEM_DB_NAME")

    db = MongoClient(
        SMART_ELEVATOR_SYSTEM_DB_URI,
        maxPoolSize=3,
        connectTimeoutMS=2500)

    return db
