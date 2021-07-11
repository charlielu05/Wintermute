# Generate HTML report using Jinja2
import pandas as pd
import numpy as np
import jinja2
import logging 
import os 
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from config import Config 
from funcs import load_pickle, s3_download, s3_upload

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def create_reports_df(df:pd.DataFrame)->pd.DataFrame:
    # generate average price
    df_avg_price= pd.DataFrame((df.groupby('cluster')
                    .agg(average_price=pd.NamedAgg(column='retailer_price', aggfunc='mean'),
                        count=pd.NamedAgg(column='gender', aggfunc='count'))))

    # generate color distribution
    df_color = (df.groupby(['cluster'])['e_color']
                    .value_counts())
    df_top3_color = (pd.DataFrame(df_color
                                .groupby('cluster')
                                .apply(lambda x: x.head(3))
                                )
                                .droplevel(1).rename(columns={'e_color': 'counts'})
                    )

    # generate gender distribution
    df_gender = pd.DataFrame((df.groupby(['cluster'])['gender']
                    .value_counts())).rename(columns={'gender': 'counts'})

    # generate brand distribution
    df_brand = (df.groupby(['cluster'])['brand']
                    .value_counts())
    df_top3_brand = (pd.DataFrame(df_brand
                                .groupby('cluster')
                                .apply(lambda x: x.head(3))
                                )
                                .droplevel(1).rename(columns={'brand': 'counts'})
                    )

    return df_avg_price, df_top3_color, df_gender, df_top3_brand
        
def plot_results(cls, features:np.array, plot_filename:str):
    # reduce the features to 2D
    log.info("PCA dimension reduce...")
    pca = PCA(n_components=2, random_state=43)
    reduced_features = pca.fit_transform(features.toarray())

    # reduce the cluster centers to 2D
    reduced_cluster_centers = pca.transform(cls.cluster_centers_)

    log.info(f"Plot and save figure as '{Config.PLOT_FILENAME}'")
    plt.title('PCA reduced view of data clusters')
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.savefig(plot_filename)

def plot_elbo(features:np.array, plot_filename:str):
    distortions = []
    K = range(1,10)
    for k in K:
        kmeanModel = MiniBatchKMeans(n_clusters=k, random_state=43)
        kmeanModel.fit(features)
        distortions.append(kmeanModel.inertia_)
    
    plt.figure(figsize=(16,8))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.savefig(plot_filename)

def generate_html_report(dataframes:list, filename:str):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('./src/report_template.html')
    # html = template.render(avg_price=df.to_html())
    html = template.render(tables= [df.to_html() for df in dataframes],
                        titles= ['na',
                                'Average price', 
                                'Top 3 Color', 
                                'Gender', 
                                'Top 3 Brands'])
    
    with open(filename, 'w') as f:
        f.write(html)

# create the HTML file
if __name__ == "__main__":
    # download model, features and result dataframe from s3 
    s3_download(Config.S3_BUCKET, 
                f"./{Config.MODEL_NAME}", 
                Config.MODEL_NAME)
    s3_download(Config.S3_BUCKET, 
                f"./{Config.TRAINING_FEATURES}", 
                Config.TRAINING_FEATURES)
    s3_download(Config.S3_BUCKET, 
                f"./{Config.RESULT_DATAFRAME_NAME}", 
                Config.RESULT_DATAFRAME_NAME)
    
    # read into environment
    log.info("Load model pickle...")
    model = load_pickle(Config.MODEL_NAME)
    log.info("Load features array pickle...")
    features = load_pickle(Config.TRAINING_FEATURES)
    log.info("Load result dataframe pickle...")
    df_results = load_pickle(Config.RESULT_DATAFRAME_NAME)

    log.info("Generate report dataframes from the cluster assignments...")
    df_avg_price, df_top3_color, df_gender, df_top3_brands = create_reports_df(df_results)
    log.info("Convert dataframes to pickle files...")

    log.info("Create PCA reduced dimensions plot...")
    plot_results(model, features, Config.PLOT_FILENAME)
  
    log.info("Create ELBO plot...")
    plot_elbo(features, Config.PLOT_ELBO_FILENAME)
    
    # generate HTML report using Jinja2
    log.info("Generate html report...")
    generate_html_report([df_avg_price, df_top3_color, df_gender, df_top3_brands],
                        Config.HTML_REPORT)

    # upload report to s3 
    log.info("Upload report to s3...")
    s3_upload(Config.S3_BUCKET, Config.HTML_REPORT)