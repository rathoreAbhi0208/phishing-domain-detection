from phishing.pipeline.training_pipeline import start_training_pipeline
from phishing.pipeline.batch_prediction import start_batch_prediction

file_path = "D:\Python\Inue\phishing_domain_detection\phishing_dataset.csv"

if __name__ == "__main__":
    try:
        #start_training_pipeline()
        output_file = start_batch_prediction(input_file_path=file_path)
        print(output_file)
        
    except Exception as e:
        print(e)
