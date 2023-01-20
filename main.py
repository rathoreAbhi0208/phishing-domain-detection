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
import os ,sys

# def test_logger_and_exception():
#     try:
#         logging.info("Starting the test_logger_and_exception")
#         result =3/0
#         print(result)
#         logging.info("Stopping test_logger_and_exception")
#     except Exception as e:

#         logging.debug(str(e))
#         raise PhishingException(e, sys)


if __name__ == "__main__":
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

    except Exception as e:
        print(e)
