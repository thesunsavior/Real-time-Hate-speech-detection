import pytchat

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from chat import stream_chat
from utils.preprocessing import preprocess_df
from model.logistic_regression import LogisticRegression
from sentence_classification import produce_classification_inference
from config import Config

config = Config()
# preprocess data
df_train = pd.read_csv(f"{config.DATA_FOLDER}/vihsd/train.csv")
df_valid = pd.read_csv(f"{config.DATA_FOLDER}/vihsd/dev.csv")

train_df = preprocess_df(df_train)
val_df = preprocess_df(df_valid)

model = LogisticRegression(train_df, val_df)
infer_fn = produce_classification_inference(model)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Establish fastapi"}


@app.get("/chat/{video_id}")
async def read_chat(video_id: str):
    chat = pytchat.create(video_id=video_id)
    return StreamingResponse(stream_chat(chat, infer_fn), media_type="text/event-stream")
