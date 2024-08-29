import os

class Config:
    MODEL_FOLDER = os.environ.get(
        'MODEL_FOLDER') or 'src/spans_tagging_service/models'
    MODEL_NAME = os.environ.get(
        'MODEL_NAME') or 'distilbert'

    SPAN_TAGGING_QUEUE = os.environ.get('SPAN_TAGGING_QUEUE') or 'span_tagging'
    VNCORE_NLP_PATH = os.environ.get('VNCORE_NLP_PATH') or 'vncorenlp/VnCoreNLP-1.1.1.jar'

    REDIS_HOST = os.environ.get('REDIS_HOST') or 'redis'
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None

    