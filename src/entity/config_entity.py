import os
from datetime import datetime
from dataclasses  import dataclass
from src.constants import *

TIMESTAMP=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
@dataclass
class Trainpipelineconfig:
    pipeline_name:str=PIPELINE_NAME
    artifact_dir=os.path.join(ARTIFACT_DIR,TIMESTAMP)
    timestamp:str=TIMESTAMP

train_pipeline_config:Trainpipelineconfig  =Trainpipelineconfig()  

@dataclass
class Dataingestionconfig:
    data_ingestion_dir=os.path.join(train_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_path=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,DATA_FILE_NAME)
    training_file_path=os.path.join(data_ingestion_dir,DATA_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path=os.path.join(data_ingestion_dir,DATA_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_RATIO
    collection_name:str=COLLECTION_NAME

@dataclass
class Datavalidationconfig:
    data_validation_dir=os.path.join(train_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
    report_file_path=os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class Datatransformationconfig:
    data_transformation_dir=os.path.join(train_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    data_transformed_train_file=os.path.join(data_transformation_dir,DATA_TRANSFORMED_DIR_NAME,TRAIN_FILE_NAME.replace('csv','npy'))
    data_transformed_test_file=os.path.join(data_transformation_dir,DATA_TRANSFORMED_DIR_NAME,TEST_FILE_NAME.replace('csv','npy'))
    data_transformed_object=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PREPROCESSING_PIPELINE_OBJECT_NAME)

@dataclass
class Modeltrainerconfig:
    model_training_dir=os.path.join(train_pipeline_config.artifact_dir,MODEL_TRAINING_DIR_NAME)
    model_file_path=os.path.join(model_training_dir,MODEL_TRAINER_TRAINED_DIR_NAME,MODEL_TRAINER_TRAINED_MODEL_FILE_NAME)
    model_min_samples_leaf=MODEL_TRAINER_MIN_SAMPLES_LEAF
    model_trainer_average_score=MODEL_TRAINER_AVERAGE_SCORE
    model_min_samples_split=MODEL_TRAINER_MIN_SAMPLES_SPLIT
    momodel_n_estimators=MODEL_TRAINER_N_ESTIMATORS
    model_config_file=MODEL_TRAINER_CONFIG_FILE
    model_random_state=MIN_SAMPLES_SPLIT_RANDOM_STATE
    model_max_depth=MIN_SAMPLES_SPLIT_MAX_DEPTH
    model_criterion=MIN_SAMPLES_SPLIT_CRITERION

@dataclass
class Modelevaluationconfig:
    model_threshhold_difference=MODEL_EVALUATION_CHANGED_THRESHHOLD
    model_bucket_name=MODEL_BUCKET_NAME
    model_key_path=MODEL_FILE_NAME

@dataclass
class Modelpusherconfig:  
    model_bucket_name=MODEL_BUCKET_NAME
    model_key_path=MODEL_FILE_NAME  



