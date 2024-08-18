import torch

from transformers import AutoModel, AutoTokenizer
from models.bert import MultiTaskModel

from vncorenlp import VnCoreNLP


def spans_inference(model, tokenizer, input_text, threshold=0.2):
    model.eval()

    annotator = VnCoreNLP("vncorenlp/VnCoreNLP-1.1.1.jar",
                          annotators="wseg", max_heap_size='-Xmx500m')
    annotator_text = annotator.tokenize(input_text)
    tokens = []
    for i in range(len(annotator_text)):
        for j in range(len(annotator_text[i])):
            tokens.append(annotator_text[i][j])

    inp = [tokenizer(text, return_tensors="pt")for text in tokens]

    labels = []
    for i in range(len(inp)):
        with torch.no_grad():
            inp_ids = inp[i]['input_ids'].squeeze(1)
            inp_att_mask = inp[i]['attention_mask']
            output = model(inp_ids, inp_att_mask)

            flatten_output = output.squeeze().cpu().numpy().flatten()

            kt = False
            for i in range(len(flatten_output)):
                if flatten_output[i] > threshold:
                    labels.append(1)
                    kt = True
                    break

            if kt == False:
                labels.append(0)

    return labels


if __name__ == '__main__':
    test_path = "data/Sequence_labeling_based_version/Word/test_BIO_Word.csv"
    model_name = "distilbert/distilbert-base-multilingual-cased"
    # Define the path to the checkpoint file
    checkpoint_path = 'DIstilBert_model_checkpoint.pt'

    input_model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    input_model.resize_token_embeddings(len(tokenizer))

    # Load the model architecture
    input_model.resize_token_embeddings(len(tokenizer))
    infer_model = MultiTaskModel(input_model=input_model)

    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    infer_model.load_state_dict(checkpoint)

    # Set the model to evaluation mode
    infer_model.eval()

    # Prepare the input data
    input_text = "vãi lồn Thảo ơiii"

    annotator = VnCoreNLP("vncorenlp/VnCoreNLP-1.1.1.jar",
                          annotators="wseg", max_heap_size='-Xmx500m')
    annotator_text = annotator.tokenize(input_text)
    tokens = []
    for i in range(len(annotator_text)):
      for j in range(len(annotator_text[i])):
        tokens.append(annotator_text[i][j])

    print(tokens)

    inp = [tokenizer(text,
                     return_tensors="pt")for text in tokens]

    threshold = 0.2
    labels = []

    # Perform inference
    for i in range(len(inp)):
      with torch.no_grad():
        inp_ids = inp[i]['input_ids'].squeeze(1)
        inp_att_mask = inp[i]['attention_mask']
        output = infer_model(inp_ids, inp_att_mask)

        flatten_output = output.squeeze().cpu().numpy().flatten()

        kt = False
        for i in range(len(flatten_output)):
          if flatten_output[i] > threshold:
            labels.append(1)
            kt = True
          break

        if kt == False:
            labels.append(0)

    print(labels)
