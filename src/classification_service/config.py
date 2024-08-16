import os


class Config:
    DATA_FOLDER = os.environ.get('DATA_FOLDER') or './data'
