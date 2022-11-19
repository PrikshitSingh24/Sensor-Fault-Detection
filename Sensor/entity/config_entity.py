from datetime import datetime
import os
from Sensor.constant import Training_pipeline
from Sensor.constant.Training_pipeline import TEST_FILE_NAME,TRAIN_FILE_NAME,FILE_NAME
from Sensor.constant.Training_pipeline import DATA_VALIDATION_DIR_NAME,DATA_VALIDATION_VALID_NAME,DATA_VALIDATION_INVALID_NAME,DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILENAME

class TrainingPipelineConfig:

    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name:str=Training_pipeline.PIPELINE_NAME
        self.artifact_dir:str=os.path.join(Training_pipeline.ARTIFACT_DIR,timestamp)
        self.timestamp: str=timestamp
        
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str=os.path.join(
            TrainingPipelineConfig.artifact_dir,Training_pipeline.DATA_INGESTION_DIR_NAME
        )  
        
        self.feature_store_file_paths: str=os.path.join(
            self.data_ingestion_dir,Training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME
        )

        self.training_file_path: str=os.path.join(
            self.data_ingestion_dir,Training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,TRAIN_FILE_NAME
        )

        self.testing_file_path: str=os.path.join(
            self.data_injestion_dir,Training_pipeline.DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME
        )

        self.train_test_split_ratio: float=Training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.collection_name: str=Training_pipeline.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
        
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,DATA_VALIDATION_VALID_NAME)

        self.invalid_data_dir:str=os.paht.join(self.data_validation_dir,DATA_VALIDATION_INVALID_NAME)

        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,TRAIN_FILE_NAME)

        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,TEST_FILE_NAME)

        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,TRAIN_FILE_NAME)

        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,TEST_FILE_NAME)

        self.drift_report_file_path:str=os.path.join(self.data_validation_dir,DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILENAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,Training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path:str=os.path.join(
            self.data_transformation_dir,Training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TRAIN_FILE_NAME.replace("csv","npy")
        )
        self.transformed_test_file_path:str=os.path.join(
            self.data_transformation_dir,Training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TEST_FILE_NAME.replace("csv","npy")
        )
        self.transformed_object_file_path:str=os.path.join(
            self.data_transformation_dir,Training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,Training_pipeline.PREPROCCESSING_OBJECT_FILE_NAME
        )

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str=os.path.join(training_pipeline_config.artifact_dir,Training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str=os.path.join(self.model_trainer_dir,Training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,Training_pipeline.MODEL_FILE_NAME)
        self.expected_accuracy: float=Training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold=Training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_SCORE
        

