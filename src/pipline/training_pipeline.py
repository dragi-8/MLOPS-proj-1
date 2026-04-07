import sys
from src.exception import MYexception
from src.logger import logging

from src.components.data_ingestion import Dataingestion
from src.components.data_validation import Datavalidation
from src.entity.config_entity import Dataingestionconfig
from src.entity.config_entity import Datavalidationconfig
from src.entity.artifact_entity import Dataingestionartifact
from src.entity.artifact_entity import Datavalidationartifact

class Trainpipeline:
    def __int__(self):
        self.data_ingestion_config=Dataingestionconfig()
        self.data_validation_config=Datavalidationconfig()


    def start_data_ingetsion(self) -> Dataingestionartifact:
        try:
            logging.info('starting data ingestion in training pipeline')
            data_ingestion=Dataingestion(data_config=Dataingestionconfig)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info('created data ingestion artifact')
            return data_ingestion_artifact
        except Exception as e:
            raise MYexception(e,sys)
        

    def   start_data_validation(self) -> Datavalidationartifact:
        try:
            logging.info('starting data validation in pipeline')
            data_validation=Datavalidation(data_validation_config=Datavalidationconfig,data_ingestion_artifact=Dataingestionartifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info('created data validation artifact')
            return data_validation_artifact
        except Exception as e:
            raise MYexception(e,sys)
        
        

        
    def run_pipeline(self)  -> None:
        try:
            data_ingestion_artifact=self.start_data_ingetsion()
            data_validation_artifact=self.start_data_validatio()
        except Exception as e:
            raise MYexception(e,sys )   
