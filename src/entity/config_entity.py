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

# @dataclass
# class Datatransormationconfig:




