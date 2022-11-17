from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.entity.config_entity import DataIngestionConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact
import os,sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split 
from Sensor.data_access.sensor_data import SensorData
from Sensor.utils.main_utils import read_yaml_file
from Sensor.constant.Training_pipeline import SCHEMA_FILE_PATH
class DataIngestion:

    def __init__(self,data_ingestion_config=DataIngestionConfig):
        try:
             self.data_ingestion_config=data_ingestion_config
             self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
            
    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info("Exporting data from Mongodb to feature store")
            sensor_data=SensorData()
            Dataframe=sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path=self.data_ingestion_config.feature_store_file_paths
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            Dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return Dataframe
        except Exception as e:
            raise SensorException(e,sys)

    def split_data_as_train_test(self,Dataframe:DataFrame)->None:

        try:
            train_set,test_set=train_test_split(
                DataFrame,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("performed train test split on the dataframe")

            logging.info("Exited split_data_as_train_test_method of the data_ingestion class")


            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise SensorData(e,sys)





    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            Dataframe=self.export_data_into_feature_store()
            Dataframe=Dataframe.drop(self._schema_config["drop_columns"],axis=1)
            self.split_data_as_train_test(Dataframe=Dataframe)
            data_ingestion_artifact= DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

