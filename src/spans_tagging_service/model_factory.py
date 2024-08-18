import torch

from config import Config
from transformers import AutoModel, AutoTokenizer
from models.bert import MultiTaskModel

config = Config()

model_huggingface = {
    "distilbert": "distilbert-base-multilingual-cased",
    "phobert": "vinai/phobert-base",
    "xlm-roberta": "xlm-roberta-base",
}
model_ckpt_paths = {
    "distilbert": f"{config.MODEL_FOLDER}/DIstilBert_model_checkpoint.pt",
    "phobert": f"{config.MODEL_FOLDER}/PhoBERT_model_checkpoint.pt",
    "xlm-roberta": f"{config.MODEL_FOLDER}/XLM-RoBERTa_model_checkpoint.pt",
}


def get_model(model_name):
    model_name = model_name.lower()
    model_hf = model_huggingface.get(model_name)
    if model_hf is None:
        raise ValueError(f"Model {model_name} not supported")

    model_ckpt_path = model_ckpt_paths[model_name]

    # Load the model architecture from hf
    input_model = AutoModel.from_pretrained(model_hf)
    tokenizer = AutoTokenizer.from_pretrained(model_hf)
    input_model.resize_token_embeddings(len(tokenizer))

    # Load pre-trained model
    model = MultiTaskModel(input_model=input_model)
    checkpoint = torch.load(model_ckpt_path, map_location='cpu')
    model.load_state_dict(checkpoint)

    return model
