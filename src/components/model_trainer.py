import os 
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from src.entity.estimator import MyModel
from src.entity.config_entity import Modeltrainerconfig
from src.entity.artifact_entity import Modeltrainerartifact, Metricartifact,Datatransformationartifact
from src.utils import save_object,load_numpy_array_data,load_object
from src.logger import logging
from src.exception import MYexception   

class Modeltrainer:
    def __init__(self,model_training_config:Modeltrainerconfig,data_transformation_artifact:Datatransformationartifact):
        

        self.model_training_config=model_training_config
        self.data_transformation_artifact=data_transformation_artifact

    

    def get_model_object_and_report(self,train_data:np.array,test_data:np.array) -> tuple[object,object]   : 
        try:
            # train_data and test_data are whole arrays where last column is the target.
            X_train = train_data[:, :-1]
            y_train = train_data[:, -1]

            X_test = test_data[:, :-1]
            y_test = test_data[:, -1]

            model = RandomForestClassifier(
                n_estimators=self.model_training_config.momodel_n_estimators,
                random_state=self.model_training_config.model_random_state,
                criterion=self.model_training_config.model_criterion,
                max_depth=self.model_training_config.model_max_depth,
                min_samples_leaf=self.model_training_config.model_min_samples_leaf,
                min_samples_split=self.model_training_config.model_min_samples_split,
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            logging.info("Model training done.")

            acc = accuracy_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            metric_artifact = Metricartifact(f1_score=f1, recall_score=rec, precision_score=prec)
            logging.info(f"Model evaluation done with accuracy score: {acc}, recall score: {rec}, precision score: {prec} and f1 score: {f1}")
            return model, metric_artifact
        except Exception as e:
            raise MYexception(e,sys) from e
        
    def initiate_model_trainer(self)->Modeltrainerartifact:
        try:
            logging.info("Model trainer initiated")
            train_data=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path) 
            test_data=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path) 

            model,metric=self.get_model_object_and_report(train_data=train_data,test_data=test_data)

            if accuracy_score(train_data[:, -1], model.predict(train_data[:, :-1])) < self.model_training_config.model_trainer_average_score:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")

            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_path)
            mymodel=MyModel(preprocessing_object=preprocessor,trained_model_object=model)
            save_object(file_path=self.model_training_config.model_file_path,obj=mymodel)
            logging.info("Model trainer artifact created")
            model_trainer_artifact=Modeltrainerartifact(model_file=self.model_training_config.model_file_path,metric=metric)
            return model_trainer_artifact
        except Exception as e:
            raise MYexception(e,sys) from e



