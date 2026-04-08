import os 
import pandas as pd
import json
import sys
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer


from src.logger import logging
from src.exception import MYexception
from src.entity.artifact_entity import Dataingestionartifact,Datavalidationartifact,Datatransformationartifact
from src.entity.config_entity import Datatransformationconfig
from src.constants import SCHEMA_FILE_PATH,TARGET_COLUMN
from src.utils.main_utils import save_object, save_numpy_array_data, read_yaml


class Datatransformation:
    def __init__(self,data_ingestion_artifact:Dataingestionartifact,data_transformation_config:Datatransformationconfig,data_validation_artifact:Datavalidationartifact):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            self._schema_file_path=read_yaml(filepath=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MYexception(e,sys)    
    
    @staticmethod
    def read_file(filepath:str) -> pd.DataFrame:
        try:
            df=pd.read_csv(filepath)
            return df
        except Exception as e:
            raise MYexception(e,sys)    
    
    def get_transformer_object(self) -> Pipeline:
        try:


            num_trans_tool=StandardScaler()
            mm_trans_tool=MinMaxScaler()

            num_col=self._schema_file_path['num_features']
            mm_col=self._schema_file_path['mm_features']
            logging.info('Got numerical and minmax columns from schema.yaml file')

            preprocessor= ColumnTransformer(
            transformers=[('standarscaler',num_trans_tool,num_col),('minmacscaler',mm_trans_tool,mm_col)],
            remainder='passthrough'
        )
            pipeline=Pipeline(steps=[('preprocessor',preprocessor)])
            logging.info('pipeline made for transformed object')
            return pipeline
        except Exception as e:
            raise MYexception(e,sys)

    def map_genders(self,df)   :
        try:
            df['Gender']=df['Gender'].map({'Male': 1, 'Female': 0})
            return df
        except Exception as e:
            raise MYexception(e,sys)

    def generate_dummies(self,df):
        try:
            df=pd.get_dummies(df,drop_first=True)
            return df
        except Exception as e:  
            raise MYexception(e,sys)

    def rename_columns(self,df):
        try:
            df.rename(columns={"Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"})
            for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
                if col in df.columns:
                    df[col]=df[col].astype(int)
            return df
        except Exception as e:
            raise MYexception(e,sys)    

    def drop_id_column(self,df):
        try:
            drop_col=self._schema_file_path['drop_columns']
            if drop_col in df.columns:
                df=df.drop(drop_col,axis=1)
            return df
        except Exception as e:
            raise MYexception(e,sys) 

    def initiate_data_transformation(self) -> Datatransformationartifact:  
        try:  

            train_df=self.read_file(filepath=self.data_ingestion_artifact.train_file_path)
            test_df=self.read_file(filepath=self.data_ingestion_artifact.test_file_path) 

            train_data_y=train_df[TARGET_COLUMN]
            train_data_x=train_df.drop(columns=[TARGET_COLUMN])
                
            test_data_y=test_df[TARGET_COLUMN]
            test_data_x=test_df.drop(columns=[TARGET_COLUMN])

            train_data_x=self.drop_id_column(train_data_x)
            test_data_x=self.drop_id_column(test_data_x)

            train_data_x=self.map_genders(train_data_x)
            train_data_x=self.generate_dummies(train_data_x)
            train_data_x=self.rename_columns(train_data_x)


            test_data_x=self.map_genders(test_data_x)
            test_data_x=self.generate_dummies(test_data_x)
            test_data_x=self.rename_columns(test_data_x)
            logging.info('all input data transformed using custom funcion in data transformation')

            preprocessor=self.get_transformer_object()


            train_data_arr=preprocessor.fit_transform(train_data_x)
            test_data_arr=preprocessor.transform(test_data_x)

            smt=SMOTEENN(sampling_strategy='minority')

            final_xtrain,final_ytrain=smt.fit_resample(train_data_arr,train_data_y)
            final_xtest,final_ytest=smt.fit_resample(test_data_arr,test_data_y)
            logging.info('applied smoteenn to handle imbalanced data')

            final_train_data=np.c_[final_xtrain,final_ytrain]
            final_test_data=np.c_[final_xtest,final_ytest]

            save_object(file_path=self.data_transformation_config.data_transformed_object,obj=preprocessor)
            save_numpy_array_data(file_path=self.data_transformation_config.data_transformed_train_file,array=final_train_data)
            save_numpy_array_data(file_path=self.data_transformation_config.data_transformed_test_file,array=final_test_data)
            logging.info('saved transformed object and transformed train and test data array')

            data_transformation_artifact=Datatransformationartifact(transformed_object_path=self.data_transformation_config.data_transformed_object,                                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file,transformed_test_file_path=self.data_transformation_config.data_transformed_test_file)
            return data_transformation_artifact
        except Exception as e:
            raise MYexception(e,sys) from e



                