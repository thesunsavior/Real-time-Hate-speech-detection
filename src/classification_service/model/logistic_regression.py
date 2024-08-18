import torch


class LogisticRegression (torch.nn.Module):
    def __init__(self, model, vectorizer):
        super(LogisticRegression, self).__init__()
        self.model = model
        self.vectorizer = vectorizer

    def forward(self, s: str):
        x = self.vectorizer.transform([s])
        return self.model.predict(x)[0]
