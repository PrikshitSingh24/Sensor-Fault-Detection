import os
from Sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
# defining common constant variable for training pipline 

TARGET_COLUMN="class"
PIPELINE_NAME:str="sensor"
ARTIFACT_DIR:str="artifact"
FILE_NAME:str="sensor.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

PREPROCCESSING_OBJECT_FILE_NAME="preproccessing.pkl"
MODEL_FILE_NAME="model.pkl"
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")
SCHEMA_DROP_COLS="drop_column"

DATA_INGESTION_COLLECTION_NAME:str="sensor"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float=0.2


DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_NAME:str="validated"
DATA_VALIDATION_INVALID_NAME:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME:str="report.yaml"


DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"

MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:str=0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_SCORE:str=0.05


