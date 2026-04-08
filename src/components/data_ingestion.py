import os 
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import MYexception
from src.entity.config_entity import Dataingestionconfig
from src.entity.artifact_entity import Dataingestionartifact

from src.data_access.proj1_data import Proj1Data

class Dataingestion:
    def __init__(self,data_config:Dataingestionconfig=Dataingestionconfig()):

        self.data_config=data_config

    def load_data_from_mongodb(self, collection_name:str = None) -> pd.DataFrame:
        try:
            data=Proj1Data()
            df=data.export_collection_as_dataframe(collection_name=Dataingestionconfig.collection_name)
            logging.info('loading data from mongodb')
            feature_store_path=Dataingestionconfig.feature_store_path
            dir_name=os.path.dirname(feature_store_path)
            os.makedirs(dir_name,exist_ok=True)
            df.to_csv(feature_store_path,index=False)
            return df
        except Exception as e:
            raise MYexception(e,sys)
    def split_data_into_train_test(self, dataframe:pd.DataFrame) -> None:
        try:
            train_data,test_data=train_test_split(dataframe,test_size=Dataingestionconfig.train_test_split_ratio)
            logging.info('Complete train ,test split on df')

            dir_path=os.path.dirname(Dataingestionconfig.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(Dataingestionconfig.training_file_path,index=False)
            test_data.to_csv(Dataingestionconfig.testing_file_path,index=False)
            logging.info('both  training and testing datasets saved')
        except Exception as e :
            raise MYexception(e,sys)   
        
    def initiate_data_ingestion(self) -> Dataingestionartifact:
        try:
            data=self.load_data_from_mongodb()
            self.split_data_into_train_test(data)
            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            data_ingestion_artifact=Dataingestionartifact(train_file_path=self.data_config.training_file_path,test_file_path=self.data_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise MYexception(e,sys)








