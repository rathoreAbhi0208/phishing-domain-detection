from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.utils import get_collection_as_dataframe
from phishing.entity import config_entity
from phishing.entity.config_entity import DataIngestionConfig
from phishing.components.data_ingestion import DataIngestion
from phishing.components.data_validation import DataValidation
from phishing.components import data_validation
from phishing.components.model_trainer import ModelTrainer
from phishing.components.data_transformation import DataTransformation
from phishing.components.model_evaluation import ModelEvaluation
from phishing.components.model_pusher import ModelPusher
import os ,sys



def start_training_pipeline():

    try:
        #test_logger_and_exception()
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        
        #data Ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        #data Validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
        data_ingestion_artifact=data_ingestion_artifact)

        data_validation_artifact = data_validation.initiate_data_validation()

        #data Transformation
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation( data_transformation_config=data_transformation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        #Model Trainer
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact =  model_trainer.initiate_model_trainer()

        #model Evaluation
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,
        data_ingestion_artifact=data_ingestion_artifact,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        #model pusher
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)

        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()

    except Exception as e:
        raise PhishingException(e, sys)