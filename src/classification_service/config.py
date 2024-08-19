import os


class Config:
    DATA_FOLDER = os.environ.get('DATA_FOLDER') or './data'
    MODEL_FOLDER = os.environ.get('MODEL_FOLDER') or './model'
    THRESHOLD = float(os.environ.get('THRESHOLD') or 0.5)
