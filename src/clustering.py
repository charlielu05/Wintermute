import pandas as pd 
import logging 
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
from config import Config
from aws import s3_download, s3_upload
from pathlib import Path

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_subset(df:pd.DataFrame, columns:list)->pd.DataFrame:
    return df[columns]

def fill_na(df:pd.DataFrame, column:str, value:str)->pd.DataFrame:
    df[[column]] = df[[column]].fillna(value)
    return df

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

def plot_results(cls, features:np.array, plot_filename:str):
    # reduce the features to 2D
    log.info("PCA dimension reduce...")
    pca = PCA(n_components=2, random_state=43)
    reduced_features = pca.fit_transform(features.toarray())

    # reduce the cluster centers to 2D
    reduced_cluster_centers = pca.transform(cls.cluster_centers_)

    log.info(f"Plot and save figure as '{Config.PLOT_FILENAME}'")
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.savefig(plot_filename)

if __name__ == "__main__":
    # download from s3
    log.info(f"Downloading csv file from s3...")
    s3_download(Config.S3_BUCKET, Config.LOCAL_PROCESSED_FILEPATH, Config.PROCESSED_FILENAME)
    
    log.info("Reading data...")
    df_train = read_data(Path(Config.LOCAL_PROCESSED_FILEPATH))
    
    log.info("Train model...")
    k_mean_model, features = model(df_train)

    log.info("Plot results...")
    plot_results(k_mean_model, features, Config.PLOT_FILENAME)

    log.info("Upload results to s3...")
    s3_upload(Config.S3_BUCKET, Config.PLOT_FILENAME, Config.PLOT_FILENAME)