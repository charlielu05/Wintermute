import pandas as pd 
import spacy
import logging 
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
from config import Config

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_subset(df:pd.DataFrame, columns:list)->pd.DataFrame:
    return df[columns]

def fill_na(df:pd.DataFrame, column:str, value:str)->pd.DataFrame:
    df[[column]] = df[[column]].fillna(value)
    return df

SUBSET_COLUMNS = ['gender', 
                'retailer_price',
                'product_name',
                'e_matched_tokens_categories_formatted',
                'e_color']

log.info("Reading data...")
raw_df = pd.read_csv("./data/processed/wintermute_data.csv")
df = (pd.read_csv("./data/processed/wintermute_data.csv")
    .pipe(get_subset, SUBSET_COLUMNS)
    .pipe(fill_na, column='gender', value='uni-sex')
    .pipe(fill_na, column='e_color', value='black')
    )

# following blog (https://sanjayasubedi.com.np/nlp/nlp-with-python-document-clustering/)

# TFIDF vectorizer
log.info("Initialize model...")
vec = TfidfVectorizer(stop_words="english")
vec.fit(df.product_name.values)
features = vec.transform(df.product_name.values)

log.info(f"Fitting K-Means with {Config.MODEL_CLUSTERS} clusters...")
cls = MiniBatchKMeans(n_clusters=Config.MODEL_CLUSTERS, random_state=43)
cls.fit(features)


# reduce the features to 2D
log.info("PCA dimension reduce...")
pca = PCA(n_components=2, random_state=43)
reduced_features = pca.fit_transform(features.toarray())

# reduce the cluster centers to 2D
reduced_cluster_centers = pca.transform(cls.cluster_centers_)

log.info(f"Plot and save figure as '{Config.PLOT_FILENAME}'")
plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
plt.savefig(Config.PLOT_FILENAME)