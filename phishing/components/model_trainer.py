from phishing.entity import artifact_entity,config_entity
from phishing.exception import PhishingException
from phishing.logger import logging
from typing import Optional
import os,sys
from sklearn.ensemble import RandomForestClassifier
from phishing import utils
from sklearn.metrics import f1_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity,
                data_transformation_artifact:artifact_entity
                ):

        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}") 
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise PhishingException(e, sys)

    
    

    def train_model(self,x,y):
        try:
            rf_clf = RandomForestClassifier()
            rf_clf.fit(x,y)
            return rf_clf
        except Exception as e:
            raise PhishingException(e, sys)


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test array")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = train_arr[:,:-1],train_arr[:,-1]

            logging.info(f"train the model")
            model = self.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating f1 Train Score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train,y_pred=yhat_train)

            logging.info(f"Calculating f1 Test score")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_train,y_pred=yhat_test)

            logging.info(f"Train Score :{f1_train_score} Test Score :{f1_test_score} ")
            #check for overfitting or expected score
            logging.info(f"Checking if our model is Underfitted or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"model is not good as it is not able to give \
                expected accuracy : {self.model_trainer_config.expected_score} : model actual score : {f1_test_score}")

            logging.info(f"Checking if our model is overfitted or not")
            diff = abs(f1_train_score-f1_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and Test score diff : {diff} is more than Overfitting Threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained Model
            logging.info(f"saving  model object")
            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)

            #prepare Artifact
            logging.info(f"Prepare Artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise PhishingException(e, sys)


