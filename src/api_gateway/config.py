import os


class Config:
    CLASSIFICATION_SERVICE_URL = os.environ.get(
        'CLASSIFICATION_SERVICE_URL') or 'http://localhost:5000'
    STORAGE_URL = os.environ.get(
        'STORAGE_URL') or 'http://localhost:5001'
