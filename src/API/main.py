from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import pytchat
from API.chat import stream_chat, stream_mock


app = FastAPI()


@app.get("/")
def read_root():
    return {"Establish fastapi"}


@app.get("/chat/{video_id}")
async def read_chat(video_id: str):
    chat = pytchat.create(video_id=video_id)
    return StreamingResponse(stream_chat(chat), media_type="text/event-stream")
