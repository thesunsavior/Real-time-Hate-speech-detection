import re

import pandas as pd


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
