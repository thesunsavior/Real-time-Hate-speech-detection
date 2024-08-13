import pytchat


def stream_chat(chat_obj):
    while chat_obj.is_alive():
        for c in chat_obj.get().items:
            yield c.message


def stream_mock():
    for i in range(10):
        yield f"Message {i}\n"


def stream(video_id):
    stream = stream_chat(video_id)
    for s in stream:
        print(s)
