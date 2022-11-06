from datetime import datetime
import os
from Sensor.constant import Training_pipeline


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




