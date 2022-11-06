from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.entity.config_entity import DataIngestionConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact
import os,sys
from pandas import DataFrame
from Sensor.data_access.sensor_data import SensorData
class DataIngestion:

    def __init__(self,data_ingestion_config=DataIngestionConfig):
        try:
             self.data_ingestion_config=data_ingestion_config
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
        pass 



    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

