import os


class Config:
    MODEL_FOLDER = os.environ.get('MODEL_FOLDER') or './model'
    MODEL_NAME = os.environ.get(
        'MODEL_NAME') or 'distilbert'
