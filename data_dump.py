import pymongo
import pandas as pd
import json


client = pymongo.MongoClient(MONGO_CLIENT)

DATA_FILE_PATH = "D:\Python\Inue\phishing_domain_detection\phishing_dataset.csv"
DATABASE_NAME = 'phishing'
COLLECTION_NAME = 'domain'


if __name__ =="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    #convert dataframe to json so that we can dump these record in mongoDb
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #insert converted data to mongoDb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)