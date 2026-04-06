import sys
from src.exception import MYexception
from src.logger import logging

from src.components.data_ingestion import Dataingestion
from src.entity.config_entity import Dataingestionconfig
from src.entity.artifact_entity import Dataingestionartifact

class Trainpipeline:
    def __int__(self):
        self.data_ingestion_config=Dataingestionconfig()


    def start_data_ingetsion(self) -> Dataingestionartifact:
        try:
            data_ingestion=Dataingestion(data_config=Dataingestionconfig)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info('created data ingestion artifact')
            return data_ingestion_artifact
        except Exception as e:
            raise MYexception(e,sys)
        
    def run_pipeline(self,)  -> None:
        try:
            data_ingestion_artifact=self.start_data_ingetsion()
        except Exception as e:
            raise MYexception(e,sys )   
