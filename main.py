from Sensor.pipeline import training_pipeline
from Sensor.pipeline.training_pipeline import TrainPipline
from Sensor.entity.config_entity import TrainingPipelineConfig,ModelPusherConfig,ModelEvauationConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from Sensor.exception import SensorException
from Sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact,ModelTrainerArtifact
from Sensor.component.data_ingestion import DataIngestion
import sys,os
from Sensor.constant import Training_pipeline
from Sensor.component.data_ingestion import DataIngestion
from Sensor.component.data_validation import DataValidation
from Sensor.component.data_transformation import DataTransformation
from Sensor.component.model_evaluation import ModelEvaluation
from Sensor.component.model_pusher import ModelPusher
from Sensor.component.model_trainer import ModelTrainer
from Sensor.ml.model.estimator import modelResolver
from Sensor.utils.main_utils import load_object
from Sensor.logger import logging
@app.get("/predict")
async def predict_round():
    try:
        model_resolver=modelResolver(model_dir=Training_pipeline.SAVED_MODEL_DIR)
        if model_resolver.is_model_exist():
            return "Model is not available."
        best_model_path=model_resolver.get_best_model_path()
        model=load_object(file_path=best_model_path)    
    except Exception as e:
        raise SensorException(e,sys)

if __name__=='__main__':
    try:
        training_pipline=TrainPipline()
        training_pipline.run_pipline()
    except Exception as e:
        raise SensorException(e,sys)    