import re

import torch
import pandas as pd

from models.dataset.text_dataset import TextSpanDataset


def preprocess_df(df: pd.DataFrame):
    # drop na
    df = df.dropna(subset=['free_text'])

    # clean the emoji
    df['free_text'] = df['free_text'].apply(
        lambda x: re.sub(r'[^\w\s#@/:%.,_-]', '', x))

    # standardize the text
    # lowercase all
    df['free_text'] = df['free_text'].apply(lambda x: x.lower())

    # separate punctuation from words
    df['free_text'] = df['free_text'].apply(
        lambda x: re.sub(r'(?<=[^\s])\s*([^\w\s])', r' \1', x))

    return df


def preprocess_str(s: str):
    # clean the emoji
    s = re.sub(r'[^\w\s#@/:%.,_-]', '', s)

    # standardize the text
    # lowercase all
    s = s.lower()

    # separate punctuation from words
    s = re.sub(r'(?<=[^\s])\s*([^\w\s])', r' \1', s)

    return s


def create_dataloader(texts, spans, batch_size, tokenizer, max_len, shuffle=True):
    dataset = TextSpanDataset(texts, spans, tokenizer, max_len)
    # return texts
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle)
    return dataloader


def prepare_data(file_path):
    df = pd.read_csv(file_path)

    # remove nan
    df = df.dropna()
    df = df.reset_index(drop=True)

    texts = df['Word'].tolist()
    spans = df['Tag'].tolist()

    # convert spans to binary representation
    binary_spans = []
    for span in spans:
        binary_span = []
        span = span.split(' ')
        for s in span:
            if s == 'O':
                binary_span.append(0)
            else:
                binary_span.append(1)
        binary_spans.append(binary_span)

    return texts, binary_spans
