import sys

from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MYexception
from src.logger import logging
from src.entity.artifact_entity import Modelpusherartifact, Modelevaluationartifact
from src.entity.config_entity import Modelpusherconfig
from src.entity.s3_estimator import Proj1Estimator

class Modelpusher:
    def __init__(self,model_pusher_config:Modelpusherconfig,model_eval_artifact:Modelevaluationartifact):
        self.model_pusher_config=model_pusher_config
        self.model_eval_artifact=model_eval_artifact
        self.s3_client=SimpleStorageService()
        self.proj1_estimator=Proj1Estimator(bucket_name=self.model_pusher_config.model_bucket_name,model_path=self.model_pusher_config.model_key_path)

    def initiate_model_pusher(self) -> Modelpusherartifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model pusher
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            print("------------------------------------------------------------------------------------------------") 
            logging.info("Uploading artifacts folder to s3 bucket")
            
            logging.info("Uploading new model to S3 bucket....")
            self.proji_estimator.save_model(from_file=self.model_eval_artifact.trained_model_path)   
            logging.info("Model upload completed")
            model_pusher_artifact=Modelpusherartifact(s3_model_path=self.model_eval_artifact.s3_model_path, bucket_name=self.model_pusher_config.model_bucket_name)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            logging.info("Exception occurred in initiate_model_pusher method of ModelPusher class")
            raise MYexception(e,sys)    
