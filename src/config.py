
class Config():
    S3_BUCKET = 'wintermute-84'
    OBJECT_NAME = 'wintermute_data'
    PROCESSED_FILENAME = (f"processed/{OBJECT_NAME}.csv")
    LOCAL_RAW_FILEPATH = (f'./data/{OBJECT_NAME}')
    LOCAL_PROCESSED_FILEPATH = (f'./data/{PROCESSED_FILENAME}')
    MODEL_CLUSTERS = 4
    PLOT_FILENAME = "k-means-result.png"
    SUBSET_COLUMNS = ['gender', 
                'retailer_price',
                'product_name',
                'e_matched_tokens_categories_formatted',
                'e_color']