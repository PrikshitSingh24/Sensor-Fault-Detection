from Sensor.constant.Training_pipeline import SCHEMA_FILE_PATH
from Sensor.entity.artifact_entity import DataIngestionArtifact,ModelPusherArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from Sensor.entity.config_entity import DataValidationConfig,ModelPusherConfig,ModelTrainerConfig,DataTransformationConfig,ModelEvauationConfig
from Sensor.logger import logging
import pandas as pd 
from Sensor.utils.main_utils import load_numpy_array_data
from Sensor.utils.main_utils import read_yaml_file,write_yaml_file
from Sensor.exception import SensorException,sys 
from scipy.stats import ks_2samp
from Sensor.ml.model.estimator import SensorModel
from Sensor.ml.metric.classification_metric import get_classification_score
from Sensor.utils.main_utils import load_object,save_object
from Sensor.ml.model.estimator import modelResolver
from Sensor.constant.Training_pipeline import TARGET_COLUMN
import shutil 
import os 

class ModelPusher:

    def __init__(self,model_pusher_config=ModelPusherConfig,
                model_evaluation_artifact=ModelEvaluationArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact 
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_path=self.model_evaluation_artifact.train_model_file_path 
            model_file_path=self.model_pusher_config.model_file_path 
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path) 

            saved_model_path=self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)  
            shutil.copy(src=trained_model_path,dst=saved_model_path)

            model_pusher_artifact=ModelPusherArtifact(saved_model_path=saved_model_path,model_file_path=model_file_path)
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)

