import torch
from transformers import AutoModel, AutoTokenizer
from models.bert import MultiTaskModel


def save_checkpoint(model, optimizer, epoch, loss, filename="checkpoint.pth"):
    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "loss": loss
    }
    torch.save(checkpoint, filename)


def load_checkpoint(model, optimizer, filename="checkpoint.pth"):
    checkpoint = torch.load(filename)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    loss = checkpoint["loss"]
    return model, optimizer, epoch, loss


def load_model(model, filename="model.pth"):
    model.load_state_dict(torch.load(filename), map_location='cpu')
    return model


def load_bert_hf(model_name="distilbert/distilbert-base-multilingual-cased",
                            filename="model.pth"):
    input_model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    input_model.resize_token_embeddings(len(tokenizer))

    model = MultiTaskModel(input_model=input_model)
    load_model(model, filename)

    return model
