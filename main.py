from Sensor.pipeline import training_pipeline
from Sensor.pipeline.training_pipeline import TrainPipline
from Sensor.entity.config_entity import TrainingPipelineConfig,ModelPusherConfig,ModelEvauationConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from Sensor.exception import SensorException
from Sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact,ModelTrainerArtifact
from Sensor.component.data_ingestion import DataIngestion
import sys,os
from Sensor.utils.main_utils import read_yaml_file 
from Sensor.constant import Training_pipeline
from Sensor.constant.application import APP_HOST,APP_PORT 
from fastapi import FastAPI
from starlette.response import RedirectResponse,Response  
from Sensor.component.data_ingestion import DataIngestion
from Sensor.component.data_validation import DataValidation
from Sensor.component.data_transformation import DataTransformation
from Sensor.component.model_evaluation import ModelEvaluation
from Sensor.component.model_pusher import ModelPusher
from Sensor.component.model_trainer import ModelTrainer
from Sensor.ml.model.estimator import modelResolver
from uvicorn import run as app_run,app 
from Sensor.utils.main_utils import load_object
from Sensor.logger import logging
from Sensor.ml.model.estimator import TargetValueMapping

def set_env_variable(env_file_path):
    env_config=read_yaml_file(env_file_path)
    os.environ['MONGO_DB_URL']=env_config['MONGO_DBB_URL']

app=FastAPI()

origin= ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_method=["*"],
    allow_header=["*"]
)
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        train_pipline=TrainPipline()
        if train_pipline.is_pipeline_running():
            return Response("training pipline is already running.")
        train_pipline.run_pipeline()
        return Response("training successfull !!")        
    except Exception as e:
        raise SensorException(e,sys)
@app.get("/predict")
async def predict_round():
    try:
        df=None 
        model_resolver=modelResolver(model_dir=Training_pipeline.SAVED_MODEL_DIR)
        if model_resolver.is_model_exist():
            return "Model is not available."
        best_model_path=model_resolver.get_best_model_path()
        model=load_object(file_path=best_model_path)    
        y_pred=model.predict(df)
        df['predicted_column']=y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)

    except Exception as e:
        raise SensorException(e,sys)

def main():
    try:
        set_env_variable(env_file_path)
        training_pipline=TrainPipline()
        training_pipline.run_pipline()
    except Exception as e:
        raise SensorException(e,sys)    

if __name__=='__main__':
    app_run(app,host=APP_HOST,port=APP_PORT)