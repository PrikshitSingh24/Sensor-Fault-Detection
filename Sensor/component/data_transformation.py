from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pandas as pd 
from imblearn.combine import SMOTETomek
import os,sys 
from sklearn.preprocessing import RobustScaler

from Sensor.constant.Training_pipeline import TARGET_COLUMN
from Sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from Sensor.entity.config_entity import DataTransformationConfig
from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.ml.model.estimator import TargetValueMapping
from Sensor.utils.main_utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
    data_transformation_config:DataTransformationConfig,):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise SensorException(e,sys) from e     
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e,sys)    

    def get_data_transformer_object(cls)->Pipeline:
        try:
            pass 
        except Exception as e:
            raise SensorException(e,sys) from e