import json
from typing import List
from dotenv import load_dotenv

from redis_om import get_redis_connection, JsonModel
from fastapi import FastAPI, HTTPException
from starlette.requests import Request



from config import Config
from utils.model_factory import get_model
from utils.span_inference import spans_inference

load_dotenv()

config = Config()

model, tokenizer = get_model(config.MODEL_NAME)
infer_fn = spans_inference(model, tokenizer)

redis = get_redis_connection(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    decode_responses=True
)

app = FastAPI()


class SpanMessage(JsonModel):
    id: int
    message: str
    spans: List[int]

    class Meta:
        database = redis




@app.post("/message")
async def post_message(request: Request):
    message = await request.json()
    
    message_id = message["id"]
    message = message["message"]

    try:
        spans = infer_fn(message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error - Model failure")

    json_message = {"id": message_id, "message": message, "spans": spans}
    print(json_message)

    # save to Redis
    try:
        span_message = SpanMessage(**json_message)
        span_message.save()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error - Redis failure")
        
    
    return json_message


@app.get("/message/{id}")
def get_message(id: str):
    span_message = SpanMessage.get(id)
    json_message = json.dumps(span_message)
    return json_message
    
    