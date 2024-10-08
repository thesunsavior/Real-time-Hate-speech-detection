import torch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression as sk_LogReg
from pyvi import ViTokenizer


class LogisticRegression (torch.nn.Module):
    def __init__(self, train_df, valid_df):
        super(LogisticRegression, self).__init__()
        self.model = sk_LogReg()

        self.vectorizer = CountVectorizer(tokenizer=ViTokenizer.tokenize)
        self.vectorizer.fit(train_df['free_text'])

        self.train_df = train_df
        self.valid_df = valid_df

        self.x_train = self.vectorizer.transform(self.train_df['free_text'])
        self.x_valid = self.vectorizer.transform(self.valid_df['free_text'])

        self.y_train = self.train_df['label_id']
        self.y_valid = self.valid_df['label_id']

        self.model.fit(self.x_train, self.y_train)

    def eval(self):
        preds = self.model.predict(self.x_valid)
        print(accuracy_score(self.y_valid, preds))
        print(classification_report(self.y_valid, preds))

    def forward(self, s: str):
        x = self.vectorizer.transform([s])
        return self.model.predict(x)[0]
