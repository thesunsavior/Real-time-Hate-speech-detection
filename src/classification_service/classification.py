import pytchat

import pickle
from fastapi import FastAPI, WebSocket

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


@app.websocket("/ws/{video_id}")
async def read_chat(websocket: WebSocket, video_id: str):
    await websocket.accept()
    chat = pytchat.create(video_id=video_id)
    while chat.is_alive():
        for c in chat.get().items:
            message = c.message
            message = infer_fn(message)
            await websocket.send_text(message)
