import os 
import certifi
import pymongo
import sys
from src.logger import  logging
from src.exception import MYexception
from src.constants import CONNECTION_URL,DB_NAME

ca=certifi.where()

class Mongodb():
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """

    client = None  # Shared MongoClient instance across all MongoDBClient instances
    def __init__(self, database_name: str = DB_NAME):
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            if Mongodb.client is None:
                url = os.getenv(CONNECTION_URL)
                if url == " ":
                    raise Exception("Could not find connection_url")
                Mongodb.client = pymongo.MongoClient(url, tlsCAFile=ca)
            self.client = Mongodb.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful.")

        except Exception as e:
            raise MYexception(e, sys)
             

                       
