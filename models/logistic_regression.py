from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from pyvi import ViTokenizer


class LogisticRegression:
    def __init__(self, train_df, valid_df):
        self.model = LogisticRegression()

        self.vectorizer = CountVectorizer(tokenizer=ViTokenizer.tokenize)
        self.vectorizer.fit(train_df['free_text'])

        self.train_df = train_df
        self.valid_df = valid_df

    def evaluate(self):
        x_train = self.vectorizer.transform(self.train_df['free_text'])
        x_valid = self.vectorizer.transform(self.valid_df['free_text'])

        y_train = self.train_df['label_id']
        y_valid = self.valid_df['label_id']

        self.model.fit(x_train, y_train)

        preds = self.model.predict(x_valid)
        print(accuracy_score(y_valid, preds))
        print(classification_report(y_valid, preds))

    def predict(self, s: str):
        x = self.vectorizer.transform([s])
        return self.model.predict(x)[0]
