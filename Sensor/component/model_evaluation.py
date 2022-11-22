from Sensor.constant.Training_pipeline import SCHEMA_FILE_PATH
from Sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from Sensor.entity.config_entity import DataValidationConfig,ModelTrainerConfig,DataTransformationConfig,ModelEvauationConfig
from Sensor.logger import logging
import pandas as pd 
from Sensor.utils.main_utils import load_numpy_array_data
from Sensor.utils.main_utils import read_yaml_file,write_yaml_file
from Sensor.exception import SensorException,sys 
from scipy.stats import ks_2samp
from Sensor.ml.model.estimator import SensorModel
from Sensor.ml.metric.classification_metric import get_classification_score
from Sensor.utils.main_utils import load_object,save_object
from Sensor.ml.model.estimator import modelResolver,TargetValueMapping
from Sensor.constant.Training_pipeline import TARGET_COLUMN

class ModelEvaluation:
    def __init__(self,model_eval_config:ModelEvauationConfig,
    data_validation_artifact:DataValidationArtifact,model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config=ModelEvauationConfig
            self.data_validation_artifact=DataValidationArtifact
            self.model_trainer_artifact=ModelTrainerArtifact

        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            valid_train_file=self.data_validation_artifact.valid_train_file_path
            valid_test_file=self.data_validation_artifact.valid_test_file_path
            train_df=pd.read_csv(valid_train_file)
            test_df=pd.read_csv(valid_test_file)
            df=pd.concat([train_df,test_df])
            model_file_path=self.model_trainer_artifact.trained_model_file_path
            model_resolver=modelResolver()
            
            if not model_resolver.is_model_exist():
                model_evaluation_artifact=ModelEvaluationArtifact(
                    is_model_accepted=True,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=model_file_path,
                    trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                    best_model_metric_artifact=None)
                return model_evaluation_artifact

            latest_model_path=model_resolver.get_best_model_path() 
            latest_model=load_object(file_path=latest_model_path)       
            model_file_path=self.model_trainer_artifact.trained_model_file_path
            model=load_object(file_path=model_file_path)
            y_true=df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict)
            y_train_pred=model.predict(df)
            y_latest_pred=latest_model.predict(df)

            trained_metric=get_classification_score(y_true,y_train_pred)
            latest_metric=get_classification_score(y_true,y_latest_pred)
            improved_accuracy=trained_metric-latest_metric
            if self.model_eval_config.change_threshold<improved_accuracy:
                is_model_accepted=True
            else:
                is_model_accepted=False 

            model_evaluation_artifact=ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=improved_accuracy,
                    best_model_path=latest_model_path,
                    trained_model_path=model_file_path,
                    trained_model_metric_artifact=trained_metric,
                    best_model_metric_artifact=latest_metric)
            model_eval_report=model_evaluation_artifact.__dict__()
            write_yaml_file(self.model_eval_config.report_file_path,model_eval_report)
            logging.info(f"Model evaluataion artifact:{model_evaluation_artifact}")        
            return model_evaluation_artifact

           

        except Exception as e:
            raise SensorException(e,sys)



