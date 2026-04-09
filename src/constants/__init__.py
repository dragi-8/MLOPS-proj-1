import os
from datetime import datetime
try:
    from dotenv import load_dotenv
    from_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(os.path.join(from_root_path, '.env'))
except ImportError:
    pass  # dotenv not installed, will rely on system env vars

#for mongodb creation

DB_NAME='PROJ-1'
COLLECTION_NAME='PROJ-1-DATA'
CONNECTION_URL='MONGODB_URL'

ARTIFACT_DIR:str= 'artifact'
PIPELINE_NAME:str=""
SCHEMA_FILE_PATH=os.path.join('config','schema.yaml')

TARGET_COLUMN='Response'
PREPROCESSING_PIPELINE_OBJECT_NAME='preprocessing.pkl'

AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"


DATA_FILE_NAME='data.csv'
TRAIN_FILE_NAME='train.csv'
TEST_FILE_NAME='test.csv'

# DATA INNGESTION RELATED CONSTANTS

DATA_INGESTION_DIR_NAME='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR='feature_store'
DATA_INGESTED_DIR='ingested'
DATA_INGESTION_TRAIN_TEST_RATIO:float=0.25


# DATA VALIDATION RELATED CONSTANTS
DATA_VALIDATION_DIR_NAME='data_validation'
DATA_VALIDATION_REPORT_FILE_NAME:str="report.yaml"


# DATA TRANFORMATION RELATED CONSTANTS
DATA_TRANSFORMATION_DIR_NAME='data_transformation'
DATA_TRANSFORMED_DIR_NAME='transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR='transformed_object'


# MODEL TRAINING RELATED CONSTANTS
MODEL_TRAINING_DIR_NAME='model_training'
MODEL_TRAINER_TRAINED_DIR_NAME='trained'
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME='model.pkl'
MODEL_TRAINER_CONFIG_FILE=os.path.join('config','model.yaml')
MODEL_TRAINER_AVERAGE_SCORE=0.6
MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_LEAF=6
MODEL_TRAINER_MIN_SAMPLES_SPLIT=7
MIN_SAMPLES_SPLIT_CRITERION='entropy'
MIN_SAMPLES_SPLIT_MAX_DEPTH=10
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101

#model_evaluation and pushing related constants
MODEL_EVALUATION_CHANGED_THRESHHOLD:float=0.02
MODEL_FILE_NAME='model.pkl'
MODEL_BUCKET_NAME='proj-1-bucket'
MODEL_PUSHER_S3_KEY='model-registry'

