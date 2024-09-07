import pika
import pickle
import pytchat

from fastapi import FastAPI, WebSocket, BackgroundTasks

import json

from model.logistic_regression import LogisticRegression
from sentence_classification import produce_classification_inference
from utils.task import queue_message
from config import Config

config = Config()

# Load up the model
input_model = pickle.load(
    open(f"{config.MODEL_FOLDER}/checkpoint/model.pkl", "rb"))
vectorizer = pickle.load(
    open(f"{config.MODEL_FOLDER}/checkpoint/vectorizer.pkl", "rb"))

model = LogisticRegression(input_model, vectorizer)
infer_fn = produce_classification_inference(model)

# Set up queue connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue='classification')

app = FastAPI()


@app.get("/")
def read_root():
    return {"Establish fastapi"}


@app.websocket("/ws/{video_id}")
async def read_chat(websocket: WebSocket, video_id: str):
    await websocket.accept()
    
    chat = pytchat.create(video_id=video_id)
    try:
        while chat.is_alive():
            for c in chat.get().items:
                message = c.message
                prediction = infer_fn(message)
                json_message = {"id": c.id,
                                "video_id": video_id,
                                "message": message,
                                "prediction": prediction}

                # queue the message if prediction is above threshold
                if prediction > config.THRESHOLD:
                    BackgroundTasks.add_task(
                        queue_message, "classification", json_message)
                    
                # directly send the message to the client
                await websocket.send_text(json.dumps(json_message))
    except BaseException as e:  # asyncio.TimeoutError and ws.close()
        print(e)
    finally:                
        await websocket.close()