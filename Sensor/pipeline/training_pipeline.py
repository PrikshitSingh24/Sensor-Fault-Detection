from Sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact
from Sensor.exception import SensorException
import sys,os
from Sensor.logger import logging
class TrainPipline:

    def __init__(self):
        training_pipline_config=TrainingPipelineConfig()
        self.data_ingestin_config=DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig)
        self.training_pipeline_config=training_pipline_config

    def start_data_ingestion(self)->DataIngestionArtifact:
            try:
                logging.info("starting data ingestion")
                logging.info("data ingestion completed")
                
            except Exception as e:
                raise  SensorException(e,sys)

    def start_data_validation(self):
            try:
                pass
            except Exception as e:
                raise  SensorException(e,sys)

    def start_data_transformation(self):
            try:
                pass
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_trainer(self):
            try:
                pass
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_evaluation(self):
            try:
                pass
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_pusher(self):
            try:
                pass
            except Exception as e:
                raise  SensorException(e,sys)
                
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e,sys)

