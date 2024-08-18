
from fastapi import FastAPI
from model_factory import get_model
from config import Config

config = Config()
app = FastAPI()

model = get_model(config.MODEL_NAME)


@app.get("/")
def read_root():
    return {"Establish fastapi"}
