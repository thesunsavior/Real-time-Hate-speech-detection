import os


class Config:
    MODEL_FOLDER = os.environ.get(
        'MODEL_FOLDER') or 'src/spans_tagging_service/models'
    MODEL_NAME = os.environ.get(
        'MODEL_NAME') or 'distilbert'
