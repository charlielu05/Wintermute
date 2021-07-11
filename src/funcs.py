import os
import boto3
from botocore.exceptions import ClientError
import logging 
import pickle

def s3_download(s3_bucket:str, filename:str, object_name:str):
    # check if directory exists, otherwise create 
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    s3 = boto3.client('s3')
    s3.download_file(s3_bucket, object_name, filename)

def s3_upload(s3_bucket:str, filename:str, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = filename

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(filename, s3_bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# save model to pickle file
def save_pickle(object, filename:str):
    pickle.dump(object, open(filename, 'wb'))

# load model from pickle file
def load_pickle(filename:str):
    object = pickle.load(open(filename, 'rb'))
    return object 