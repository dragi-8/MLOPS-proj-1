import os 
import pandas as pd
import json
import sys

from src.logger import logging
from src.exception import MYexception
from src.entity.artifact_entity import Dataingestionartifact,Datavalidationartifact
from src.entity.config_entity import Datavalidationconfig
from src.utils.main_utils import read_yaml
from src.constants import SCHEMA_FILE_PATH



class Datavalidation:
    def __init__(self,data_validation_config:Datavalidationconfig,data_ingestion_artifact:Dataingestionartifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.__schema_path=read_yaml(filepath=SCHEMA_FILE_PATH)

        except Exception as e:
            raise MYexception(e,sys)   

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception  """ 
        try:

            status=len(dataframe.columns) == len(self.__schema_path['columns'])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise MYexception(e, sys)
    def is_column_exists(self,dataframe:pd.DataFrame) -> bool:
        try:
            dataframe_columns=dataframe.columns 
            missing_cat_columns=[]
            missing_num_columns=[]
            for column in  self.__schema_path['numerical_columns']:
                if column not in dataframe_columns :
                    missing_num_columns.append(column)
                if len(missing_num_columns)>0:
                    logging.info(f'missing numerical columns :{missing_num_columns}')    
            for column in self.__schema_path['categorical_columns']:
                if column not in dataframe_columns :
                    missing_num_columns.append(column)
                if len(missing_cat_columns)>0:
                    logging.info(f'missing numerical columns :{missing_cat_columns}')   
            return False if len(missing_num_columns)>0 or len (missing_cat_columns)  >0 else True
        except Exception as e:
            raise MYexception(e, sys)
    @staticmethod    
    def load_data(file_path:str)   -> pd.DataFrame:
        try :
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            raise MYexception(e, sys)
    def initiate_data_validation(self):
        try:
            train_data,test_data=(self.load_data(file_path=self.data_ingestion_artifact.train_file_path),self.load_data(file_path=self.data_ingestion_artifact.test_file_path))
            error_msg=""

            status=self.validate_number_of_columns(train_data)
            if status:
                logging.info('all columns are present in training data ')
            else:
                error_msg +="some columns are missing in training data"
            status=self.validate_number_of_columns(test_data)
            if status:
                logging.info('all columns are present in testing data ')
            else:
                error_msg +="some columns are missing in testingg data"
            status=self.is_column_exists(train_data) 
            if status:
                logging.info('all cat/num columns are present in training data ')
            else:
                error_msg +="some columns are missing in training data"  
            status=self.is_column_exists(test_data)   
            if status:
                logging.info('all cat/num columns are present in testing data ')
            else:
                error_msg +="some columns are missing in training data"  

            valiadtion_status=len(error_msg) ==0

            data_validation_artifact=Datavalidationartifact(validation_error_msg=error_msg,validation_condition=valiadtion_status,report_file_path=self.data_validation_config.report_file_path) 
            dir_name=os.path.dirname(self.data_validation_config.report_file_path)  
            os.makedirs(dir_name,exist_ok=True)
            validation_report={"data_validation_status":valiadtion_status,
                               "error_msg":error_msg}
            with open(self.data_validation_config.report_file_path,"w")    as f:
                json.dump(validation_report,f)
            return data_validation_artifact
        except Exception as e:
            raise MYexception(e, sys)
       



