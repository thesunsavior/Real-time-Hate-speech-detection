def stream_chat(chat_obj, process_fn: callable = None):
    while chat_obj.is_alive():
        for c in chat_obj.get().items:
            message = c.message
            if process_fn:
                message = process_fn(message)
                print(message)
            yield str(message).encode("utf-8", "ignore")

    yield "Chat has ended"
