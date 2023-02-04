from phishing.exception import PhishingException
from phishing.logger import logging
from phishing.predictor import ModelResolver
from phishing.utils import load_object
import pandas as pd
from datetime import datetime
import os, sys
import numpy as np


PREDICTION_DIR = "prediction"
PREDICTION_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"

def start_batch_prediction(input_file_path):
    try:

        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating Model Resolver Object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)

        logging.info(f"Loading Transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())

        input_feature_name = list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_name])

        logging.info(f"Loading Model to make prediction ")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr).astype('int')

        logging.info(f"Loading Target Encoder to convert predicted into categorical")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())
        

        cat_prediction = target_encoder.inverse_transform(prediction)
        

        df['prediction'] = prediction
        df['cat_pred'] = cat_prediction
        
        

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
        


        
    except Exception as e:
        PhishingException(e, sys)
