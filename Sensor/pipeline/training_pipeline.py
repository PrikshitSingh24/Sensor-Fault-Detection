from Sensor.entity.config_entity import TrainingPipelineConfig,ModelPusherConfig,ModelEvauationConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from Sensor.exception import SensorException
from Sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact,ModelTrainerArtifact
from Sensor.component.data_ingestion import DataIngestion
import sys,os
from Sensor.cloud_storage.x3_syncer import S3Sync
from Sensor.component.data_ingestion import DataIngestion
from Sensor.component.data_validation import DataValidation
from Sensor.component.data_transformation import DataTransformation
from Sensor.component.model_evaluation import ModelEvaluation
from Sensor.component.model_pusher import ModelPusher
from Sensor.component.model_trainer import ModelTrainer
from Sensor.constant.s3_bucket import TRAINING_BUCKET_NAME,PREDICTION_BUCKET_NAME
from Sensor.logger import logging
from Sensor.constant.Training_pipeline import SAVED_MODEL_DIR

class TrainPipline:
    is_pipeline_running=False 
    def __init__(self):
        training_pipline_config=TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self)->DataIngestionArtifact:
            try:
                self.data_ingestin_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
                logging.info("starting data ingestion")
                data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestin_config)
                data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
                logging.info("data ingestion completed")
                return data_ingestion_artifact
            except Exception as e:
                raise  SensorException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
            try:
                data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipline_config)
                data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
                )
                data_validation_artifact=data_validation.initiate_data_validation()
                return data_validation_artifact
            except Exception as e:
                raise  SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
            try:
                data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipline_config)
                data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config)
                data_transformation_artifact=data_transformation.initiate_data_transformation()
                return data_transformation_artifact
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
            try:
                model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipline_config)
                model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
                model_trainer_artifact=model_trainer.initiate_model_trainer()
                return model_trainer_artifact
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                model_trainer_artifact:ModelTrainerArtifact):
            try:
                model_eval_config=ModelEvauationConfig(self.training_pipeline_config)
                model_eval=ModelEvaluation(model_eval_config,data_validation_artifact,model_trainer_artifact)
                model_eval_artifact=model_eval.initiate_model_evaluation()
                return model_eval_artifact
            except Exception as e:
                raise  SensorException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
            try:
                model_pusher_config=ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
                model_pusher=ModelPusher(model_pusher_config,model_evaluation_artifact)
                model_pusher_artifact=model_pusher.initiate_model_pusher()
                return model_pusher_artifact
            except Exception as e:
                raise  SensorException(e,sys)
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)            
                
    def run_pipeline(self):
        try:
            TrainPipline.is_pipeline_running=True 
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)

            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact=self.start_model_evaluation(data_validation_artifact,model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Model is not better than the best model")
            model_pusher_artifact=self.start_model_pusher(model_eval_artifact) 
            TrainPipline.is_pipeline_running=False 
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()   
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            raise SensorException(e,sys)

