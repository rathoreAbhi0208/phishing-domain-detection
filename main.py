from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.utils import get_collection_as_dataframe
from phishing.entity import config_entity
from phishing.entity.config_entity import DataIngestionConfig
from phishing.components.data_ingestion import DataIngestion
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


        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        print(data_ingestion.initiate_data_ingestion())
    except Exception as e:
        print(e)
