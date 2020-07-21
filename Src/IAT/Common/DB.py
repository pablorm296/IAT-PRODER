import pymongo
import os
import datetime

from IAT.Config import Reader

# Read config
# Check if we are in a test env
if os.environ["FLASK_DEBUG_IAT"] == "True":
    ConfigReader = Reader(path = "./Debug", load = "all")
else:
    ConfigReader = Reader(path = None, load = "all")

# Define global config variables
CONFIG = ConfigReader.Config
MONGO_URI = ConfigReader.Mongo_Uri
STIMULI_WORDS = CONFIG["stimuli"]["words"]
STIMULI_IMAGES = CONFIG["stimuli"]["images"]
MONGO_DB = CONFIG["app"]["mongo_db_name"]
MONGO_USERS_COLLECTION = CONFIG["app"]["mongo_users_collection"]
MONGO_RESULTS_COLLECTION = CONFIG["app"]["mongo_results_collection"]

class MongoConnector:
    
    def __init__(self, targetDB: str, targetCollection: str, mongoUri: str):
        """Open a New Mongo Connector

        This class wraps around pymongo's MongoClient. It automattically opens the specified database and collections,
        while providing a handy close method.

        Args:
            targetDB (str): Name of the target database
            targetCollection (str): Name of the target collection
            mongoUri (str): URI ff the Mongo Server
        """

        # Open a new MongoClient
        self.MongoClient = pymongo.MongoClient(mongoUri)
        # Set target DB
        self.__targetDB = targetDB
        self.__setattr__(self, targetDB, self.MongoClient[targetDB])
        self.db = self.__getattribute__(targetDB)
        # Set target Collection
        self.__targetCollection = targetCollection
        self.__setattr__(self, targetCollection, self.MongoClient[targetDB][targetCollection])
        self.collection = self.__getattribute__(targetCollection)

    def close(self):

        # Close mongo client
        self.MongoClient.close()
        self.MongoClient = None

        # Set to none the target DB and target collection
        self.__setattr__(self, self.__targetDB, None)
        self.__setattr__(self, self.__targetCollection, None)
        self.db = None
        self.collection = None

class DBShortcuts:

    @staticmethod
    def updateLastUserView(view: str, user_id: str):
        # Open new connection
        MongoConnection = MongoConnector(MONGO_DB, MONGO_USERS_COLLECTION, MONGO_URI)
        # Update user in db (add one to hits, update last seen datetime, and update last view)
        updateResults = MongoConnection.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "last_seen": datetime.datetime.utcnow(),
                    "last_view": view
                },
                "$inc": {
                    "hits": 1
                }
            }
        )
        # Check update operation
        if updateResults.modified_count < 1:
            MongoConnection.close()
            return False
        else:
            MongoConnection.close()
            return True