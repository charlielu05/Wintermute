import boto3
import json
import logging 
import os
import pandas as pd 
from aws import s3_download, s3_upload
from config import Config 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def read_file(filepath:str):
    # read the file as list of dicts
    with open(filepath) as f:
        data = [json.loads(line) for line in f]

    log.info(f"Converting to pandas dataframe")
    # use python to convert to pandas dataframe
    df = pd.DataFrame(data)

    return df 
    
def save_file(df:pd.DataFrame, filepath:str):
    # check if filepath exists, create if not
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    # save pandas dataframe as csv

    df.to_csv(filepath)

if __name__ == "__main__":
    # download from s3
    log.info(f"Downloading raw file from s3...")
    s3_download(Config.S3_BUCKET, Config.LOCAL_RAW_FILEPATH, Config.OBJECT_NAME)
    
    # convert to pandas dataframe
    log.info(f"Reading file from {Config.LOCAL_RAW_FILEPATH}")
    df = read_file(Config.LOCAL_RAW_FILEPATH)
    
    # save dataframe as csv
    log.info(f"Saving dataframe to {Config.LOCAL_PROCESSED_FILEPATH}")
    save_file(df, Config.LOCAL_PROCESSED_FILEPATH)
    
    # upload to s3
    log.info(f"Uploading file to s3...")
    s3_upload(Config.S3_BUCKET,Config.LOCAL_PROCESSED_FILEPATH, Config.PROCESSED_FILENAME)