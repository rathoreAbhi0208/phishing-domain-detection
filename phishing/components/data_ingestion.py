from phishing import utils
from phishing.entity import config_entity
from phishing.entity import artifact_entity
from phishing.exception import PhishingException
from phishing.logger import logging
import pandas as pd
import numpy as np
import os,sys
from sklearn.model_selection import train_test_split

class DataIngestion:
    
    
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} DataIngestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise PhishingException(e, sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            #exporting collection data as pandas dataframe
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)

            logging.info(f"Save data in feature store")
            #save data in feature Store
            df.replace(to_replace='na',value=np.NAN,inplace=True)

            logging.info(f"Create Feature Store folder if not available")
            #create feature store folder
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            
            logging.info(f"Save df to feature store folder")
            #Saving df to feature folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info(f"Splitting dataset into train test")
            #split data into train test
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size)

            logging.info(f"Create dataset directory")
            #create dataset directory
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info(f"Save df to feature store folder")
            #Save df to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #Prepare artifact

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise PhishingException(error_message=e, error_detail=sys)