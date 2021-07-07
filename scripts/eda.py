import boto3
import json
import logging 
import os
import pandas as pd 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

INPUT_FILEPATH = './data/wintermute_data'
OUTPUT_FILEPATH = './data/wintermute.csv'

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
    df = read_file(INPUT_FILEPATH)
    save_file(df, OUTPUT_FILEPATH)
