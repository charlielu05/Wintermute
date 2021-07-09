
class Config():
    S3_BUCKET = 'wintermute-84'
    OBJECT_NAME = 'wintermute_data'
    PROCESSED_FILENAME = (f"processed/{OBJECT_NAME}.csv")
    LOCAL_INPUT_FILEPATH = (f'./data/{OBJECT_NAME}')
    LOCAL_OUTPUT_FILEPATH = (f'./data/{PROCESSED_FILENAME}')
    MODEL_CLUSTERS = 4
    PLOT_FILENAME = "k-means-result.png"