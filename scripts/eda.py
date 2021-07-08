import boto3
import json
import logging 
import os
import pandas as pd 
from botocore.exceptions import ClientError
from src.config import Config 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def s3_download(s3_bucket:str, filename:str, object_name:str):
    s3 = boto3.client('s3')
    s3.download_file(s3_bucket, object_name, filename)

def s3_upload(s3_bucket:str, filename:str, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    log.info(f"Uploading {filename} to s3")
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(filename, s3_bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def read_file(filepath:str):
    # read the file as list of dicts
    log.info(f"Reading file from {filepath}")
    with open(filepath) as f:
        data = [json.loads(line) for line in f]

    log.info(f"Converting to pandas dataframe")
    # use python to convert to pandas dataframe
    df = pd.DataFrame(data)

    return df 
    
def save_file(df:pd.DataFrame, filepath:str):
    # save pandas dataframe as csv
    log.info(f"Saving dataframe to {filepath}")
    df.to_csv(filepath)

if __name__ == "__main__":
    # download from s3
    s3_download(Config.S3_BUCKET, Config.LOCAL_INPUT_FILEPATH, Config.OBJECT_NAME)
    # convert to pandas dataframe
    df = read_file(Config.LOCAL_INPUT_FILEPATH)
    # save dataframe as csv
    save_file(df, Config.LOCAL_OUTPUT_FILEPATH)
    # upload to s3
    s3_upload(Config.S3_BUCKET,Config.LOCAL_OUTPUT_FILEPATH, Config.PROCESSED_FILENAME)