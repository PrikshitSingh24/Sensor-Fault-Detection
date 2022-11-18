from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import pandas as pd 
from imblearn.combine import SMOTETomek
import numpy as np
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
            robust_scaler=RobustScaler()
            simple_imputer=SimpleImputer(strategy="constant",fill_value=0)
            preprocessor=Pipeline(
                steps=[("Imputer",simple_imputer),
                ("RobustScaler",robust_scaler)
                ]
            )
            return preprocessor
        except Exception as e:
            raise SensorException(e,sys) from e

    def initiate_data_transformation(self,)->DataTransformationArtifact:
            try:
                train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
                test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
                processor=self.get_data_transformer_object()
                input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df=train_df[TARGET_COLUMN]

                target_feature_train_df=target_feature_train_df.replace(TargetValueMapping().to_dict())

                input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_test_df=test_df[TARGET_COLUMN]

                target_feature_test_df=target_feature_test_df.replace(TargetValueMapping().to_dict())

                preprocessor_object=processor.fit(input_feature_train_df)
                transformed_input_train_features=preprocessor_object.transform(input_feature_train_df)
                transformed_input_test_features=preprocessor_object.transform(input_feature_test_df)
                smt=SMOTETomek(sampling_strategy="minority")

                input_feature_train_final,target_feature_train_final=smt.fit_resample(
                    transformed_input_train_features,target_feature_train_df
                )
                input_feature_test_final,target_feature_test_final=smt.fit_resample(
                    transformed_input_test_features,target_feature_test_df
                )

                train_arr=np.c_[ input_feature_train_final,np.array(target_feature_train_final)]
                test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]

                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr) 
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)  
                save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object) 
                
                data_transformation_artifact=DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                )          
                logging.info(f"data transformation artifact:{data_transformation_artifact}")
                return data_transformation_artifact
            except Exception as e:
                raise SensorException(e,sys) from e    