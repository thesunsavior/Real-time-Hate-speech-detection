import torch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression as sk_LogReg
from pyvi import ViTokenizer


class LogisticRegression (torch.nn.Module):
    def __init__(self, model, vectorizer):
        super(LogisticRegression, self).__init__()
        self.model = model
        self.vectorizer = vectorizer

    def forward(self, s: str):
        x = self.vectorizer.transform([s])
        return self.model.predict(x)[0]
