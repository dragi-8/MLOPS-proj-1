import sys
import pandas as pd
import numpy as np
from typing import Optional
from src.logger import logging
from src.configuration.mongo_db_connection import Mongodb
from src.constants import DB_NAME
from src.exception import MYexception

class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.client=Mongodb(database_name=DB_NAME)
        except Exception as e :
            raise MYexception(e,sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """    
        try :
            if database_name is None:
                collection=self.client.database[collection_name]
            else : 
                collection = self.client[database_name][collection_name]  

            logging.info('fetching data from mongodb')
            df=pd.DataFrame(list(collection.find()))
            print('fetched data from db')
            if 'id 'in df.columns.to_list():
                df=df.drop(columns=['id'],axis=1)
            df.replace({"na":np.nan},inplace=True) 
            return df
        except Exception as e:
            raise MYexception(e,sys)   




