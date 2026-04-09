import sys
from src.exception import MYexception
from src.logger import logging

from src.components.data_ingestion import Dataingestion
from src.components.data_validation import Datavalidation
from src.components.data_transformation import Datatransformation
from src.components.model_trainer import Modeltrainer
from src.components.model_evaluation import ModelEvaluation
# from src.components.model_pusher import Modelpusher

from src.entity.config_entity import Dataingestionconfig
from src.entity.config_entity import Datavalidationconfig,Datatransformationconfig,Modeltrainerconfig,Modelevaluationconfig


from src.entity.artifact_entity import Dataingestionartifact,Datatransformationartifact
from src.entity.artifact_entity import Datavalidationartifact,Modeltrainerartifact,Modelevaluationartifact

class Trainpipeline:
    def __init__(self):
        self.data_ingestion_config=Dataingestionconfig()
        self.data_validation_config=Datavalidationconfig()
        self.data_transformation_config=Datatransformationconfig()
        self.model_trainer_config=Modeltrainerconfig()
        self.model_evaluation_config=Modelevaluationconfig()


    def start_data_ingetsion(self) -> Dataingestionartifact:
        try:
            logging.info('starting data ingestion in training pipeline')
            data_ingestion=Dataingestion(data_config=Dataingestionconfig())
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info('created data ingestion artifact')
            return data_ingestion_artifact
        except Exception as e:
            raise MYexception(e,sys)
        

    def   start_data_validation(self, data_ingestion_artifact: Dataingestionartifact) -> Datavalidationartifact:
        try:
            logging.info('starting data validation in pipeline')
            data_validation=Datavalidation(data_validation_config=Datavalidationconfig(), data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info('created data validation artifact')
            return data_validation_artifact
        except Exception as e:
            raise MYexception(e,sys)
        
    def start_data_transformation(self, data_ingestion_artifact: Dataingestionartifact, data_validation_artifact: Datavalidationartifact) -> Datatransformationartifact: 
        try:
            logging.info('starting data transformation pipeline')  
            data_tranformation=Datatransformation(data_ingestion_artifact=data_ingestion_artifact, data_transformation_config=Datatransformationconfig(), data_validation_artifact=data_validation_artifact) 
            data_transformer_artifact=data_tranformation.initiate_data_transformation()
            logging.info('completed data transformation')
            return data_transformer_artifact
        except Exception as e:
            raise MYexception(e,sys)
    
    def start_model_trainer(self, data_transformation_artifact: Datatransformationartifact) -> Modeltrainerartifact:
        try:
            logging.info('starting model trainer pipeline')
            model_trainer=Modeltrainer(model_training_config=Modeltrainerconfig(), data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info('completed model trainer pipeline')
            return model_trainer_artifact
        except Exception as e:
            raise MYexception(e,sys)

        def start_model_evaluation(self, data_ingestion_artifact:Dataingestionartifact, model_trainer_artifact:Modeltrainerartifact) -> Modelevaluationartifact:
            try:
                logging.info('starting model evaluation pipeline')
                model_evaluation=ModelEvaluation(model_eval_config=self.model_evaluation_config, data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact)
                model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
                logging.info('completed model evaluation pipeline')
                return model_evaluation_artifact
            except Exception as e:
                raise MYexception(e,sys)
        
    def run_pipeline(self)  -> None:
        try:
            data_ingestion_artifact=self.start_data_ingetsion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact)
            logging.info('training pipeline completed')

            
        except Exception as e:
            raise MYexception(e,sys )   
