import json
import pickle
import pytchat
import pika

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect

from connection_manager import ConnectionManager
from model.logistic_regression import LogisticRegression
from sentence_classification import produce_classification_inference
from utils.task import queue_message
from config import Config


load_dotenv()
config = Config()

# Load up the model
input_model = pickle.load(
    open(f"{config.MODEL_FOLDER}/checkpoint/model.pkl", "rb"))
vectorizer = pickle.load(
    open(f"{config.MODEL_FOLDER}/checkpoint/vectorizer.pkl", "rb"))

model = LogisticRegression(input_model, vectorizer)
infer_fn = produce_classification_inference(model)


# Set up queue connection
connection_params = pika.ConnectionParameters(
    host='localhost',
    port=5672,
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='classification')

app = FastAPI()

# Connection manager to keep track of active connections
connection_manager = ConnectionManager()


@app.get("/")
def read_root():
    return {"Establish fastapi"}


@app.websocket("/ws/{video_id}")
async def read_chat(websocket: WebSocket, video_id: str, background_tasks: BackgroundTasks):
    if video_id not in connection_manager.video_active_connections:
        connection_manager.add_video(video_id)

    await connection_manager.connect(websocket, video_id)

    chat = pytchat.create(video_id=video_id)
    try:
        while chat.is_alive():
            for c in chat.get().items:
                message = c.message
                prediction = infer_fn(message)
                json_message = {"id": str(c.id),
                                "video_id": video_id,
                                "message": message,
                                "prediction": str(prediction)}
                
                # queue the message if prediction is above threshold
                if prediction > config.THRESHOLD:
                    background_tasks.add_task(
                        queue_message, channel, "classification", json_message)

                await connection_manager.broadcast(json.dumps(json_message), video_id)

    except WebSocketDisconnect:  # asyncio.TimeoutError and ws.close()
        connection_manager.disconnect(websocket, video_id)
        print("client exited")
