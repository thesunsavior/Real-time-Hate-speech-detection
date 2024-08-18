import pytchat

import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from chat import stream_chat
from model.logistic_regression import LogisticRegression
from sentence_classification import produce_classification_inference
from config import Config

config = Config()
input_model = pickle.load(open(f"{config.MODEL_FOLDER}/model.pkl", "rb"))
vectorizer = pickle.load(open(f"{config.MODEL_FOLDER}/vectorizer.pkl", "rb"))

model = LogisticRegression(input_model, vectorizer)
infer_fn = produce_classification_inference(model)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Establish fastapi"}


@app.get("/chat/{video_id}")
async def read_chat(video_id: str):
    chat = pytchat.create(video_id=video_id)
    return StreamingResponse(stream_chat(chat, infer_fn), media_type="text/event-stream")
