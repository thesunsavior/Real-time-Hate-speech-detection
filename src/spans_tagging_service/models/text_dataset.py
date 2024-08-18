import torch


class TextSpanDataset(torch.utils.data.Dataset):
    def __init__(self, texts, spans, tokenizer, max_len):
        self.texts = [tokenizer(text,
                                padding='max_length',
                                max_length=64, truncation=True,
                                return_tensors="pt")for text in texts]
        self.spans = []

        for span in spans:
            if len(span) < max_len:
                self.spans.append(span + [0] * (max_len - len(span)))
            else:
                self.spans.append(span[:max_len])

        self.spans = torch.tensor(self.spans)

    def __len__(self):
        return len(self.spans)

    def __getitem__(self, index):
        return self.texts[index], self.spans[index]
