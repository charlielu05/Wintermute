
class Config():
    S3_BUCKET = 'wintermute-84'
    OBJECT_NAME = 'wintermute_data'
    PROCESSED_FILENAME = (f"processed/{OBJECT_NAME}.csv")
    LOCAL_RAW_FILEPATH = (f'./data/{OBJECT_NAME}')
    LOCAL_PROCESSED_FILEPATH = (f'./data/{PROCESSED_FILENAME}')
    MODEL_CLUSTERS = 5
    SUBSET_COLUMNS = ['brand',
                'gender', 
                'retailer_price',
                'product_name',
                'e_matched_tokens_categories_formatted',
                'e_color']

    # pickled filenames
    MODEL_NAME = 'model.pkl'
    RESULT_DATAFRAME_NAME = 'df_result.pkl'
    TRAINING_FEATURES = 'train_features.pkl'

    # Report filenames
    PLOT_FILENAME = "k-means-result.png"
    PLOT_ELBO_FILENAME = "k-means-elbo.png"
    HTML_REPORT = "wintermute.html"

    