from utils.preprocessing import preprocess_str


def produce_classification_inference(model):
    def inference(text: str):
        processed_txt = preprocess_str(text)
        return model(processed_txt)
    return inference
