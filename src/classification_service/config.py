import os


class Config:
    DATA_FOLDER = os.environ.get('DATA_FOLDER') or './data'
    MODEL_FOLDER = os.environ.get('MODEL_FOLDER') or './model'
