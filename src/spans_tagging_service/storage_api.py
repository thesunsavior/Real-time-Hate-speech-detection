import json

from fastapi import FastAPI

from consume import SpanMessage

app = FastAPI()


@app.get("/message/{id}")
def get_message(id: str):
    span_message = SpanMessage.get(id)
    json_message = json.dumps(span_message)
    return json_message
