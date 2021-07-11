import pandas as pd 
import logging 
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from config import Config
from funcs import s3_download, s3_upload, save_pickle
from pathlib import Path

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_subset(df:pd.DataFrame, columns:list)->pd.DataFrame:
    return df[columns]

def fill_na(df:pd.DataFrame, column:str, value:str)->pd.DataFrame:
    df[[column]] = df[[column]].fillna(value)

    return df

def df_to_pickle(df:pd.DataFrame, filename:str):
    return df.to_pickle(filename)

def read_data(filepath:Path)->pd.DataFrame:
    df = (pd.read_csv(filepath)
        .pipe(get_subset, Config.SUBSET_COLUMNS)
        .pipe(fill_na, column='gender', value='uni-sex')
        .pipe(fill_na, column='e_color', value='black')
        )

    return df 

def model(df:pd.DataFrame):
    # following blog (https://sanjayasubedi.com.np/nlp/nlp-with-python-document-clustering/)
    # TFIDF vectorizer
    log.info("Initialize model...")
    vec = TfidfVectorizer(stop_words="english")
    vec.fit(df.product_name.values)
    features = vec.transform(df.product_name.values)

    log.info(f"Fitting K-Means with {Config.MODEL_CLUSTERS} clusters...")
    cls = MiniBatchKMeans(n_clusters=Config.MODEL_CLUSTERS, random_state=43)
    cls.fit(features)

    return cls, features

def get_prediction(model, features:np.array)->np.array:
    return model.predict(features)

def append_col_to_df(df:pd.DataFrame, column_name:str, data:np.array)->pd.DataFrame:
    return df.assign(**{column_name:data})

if __name__ == "__main__":
    # download from s3
    log.info(f"Downloading csv file from s3...")
    s3_download(Config.S3_BUCKET, Config.LOCAL_PROCESSED_FILEPATH, Config.PROCESSED_FILENAME)
    
    log.info("Reading data...")
    df_train = read_data(Path(Config.LOCAL_PROCESSED_FILEPATH))
    
    log.info("Train model...")
    k_mean_model, features = model(df_train)

    log.info("Get cluster assignment from model...")
    prediction = get_prediction(k_mean_model, features)

    # Save model as pickle file and upload to s3
    log.info("Save model as pickle...")
    save_pickle(k_mean_model, Config.MODEL_NAME)
    
    log.info("Upload pickeld model to s3...")
    s3_upload(Config.S3_BUCKET, Config.MODEL_NAME)

    # Save training features as pickle and upload to s3
    log.info("Saving training features as pickle...")
    save_pickle(features, Config.TRAINING_FEATURES)

    log.info("Upload pickled features to s3...")
    s3_upload(Config.S3_BUCKET, Config.TRAINING_FEATURES)

    # get results dataframe, convert to pickle and upload to s3
    log.info("Combine cluster assignments into dataframe...")
    df_results = append_col_to_df(df_train, 'cluster', prediction)

    log.info("Save results dataframe as pickle...")
    save_pickle(df_results, Config.RESULT_DATAFRAME_NAME)

    log.info("Upload results dataframe to s3...")
    s3_upload(Config.S3_BUCKET, Config.RESULT_DATAFRAME_NAME)