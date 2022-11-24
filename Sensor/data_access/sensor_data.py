from argparse import OPTIONAL
from Sensor.configuration.mongo_db_connection import MongoDBClient
from Sensor.constant.database import DATABASE_NAME
from Sensor.exception import SensorException
from typing import Optional
import sys,os
import pandas as pd
import numpy as np 
class SensorData:
    def __init__(self):
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e,sys)
    
    def export_collection_as_dataframe(self,collection_name:str,database_name: Optional[str]=None)->pd.DataFrame:
        try:

            if database_name is None:
                collection=self.mongo_client.database[collection]

            else:
                collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)

            df.replace({"na":np.nan},inplace=True)   

            return df 
        except Exception as e:
            raise SensorException(e,sys)
                        