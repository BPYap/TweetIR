import pickle
import re

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import Booster, XGBClassifier


DATA_DIR = "../data/"
TRAIN_PATH = DATA_DIR + "twitter-airline-sentiment.csv"
EVALUATION_PATH = DATA_DIR + "evaluation_set.csv"
MODEL_DIR = "../model/"
XGBOOST_MODEL_PATH = MODEL_DIR + "xgb.bst"
TFIDF_MODEL_PATH = MODEL_DIR + "tfidf.pkl"

nltk.download('stopwords')
nltk.download('wordnet')


def preprocess(sentence):
    stemmer = WordNetLemmatizer()

    # Converting to Lowercase
    sentence = sentence.lower()

    # remove punctuation
    sentence = re.sub(r'[^\w\s]', ' ', sentence)

    # Remove all the special characters
    document = re.sub(r'\W', ' ', sentence)

    # remove all single characters
    sentence = re.sub(r'\s+[a-zA-Z]\s+', ' ', sentence)

    # Remove single characters from the start
    sentence = re.sub(r'\^[a-zA-Z]\s+', ' ', sentence)

    # Substituting multiple spaces with single space
    sentence = re.sub(r'\s+', ' ', sentence, flags=re.I)

    # Removing prefixed 'b'
    sentence = re.sub(r'^b\s+', '', sentence)

    # Lemmatization
    sentence = sentence.split()
    sentence = [stemmer.lemmatize(word) for word in sentence]
    sentence = ' '.join(sentence)

    return sentence


_cached_model = None
_cached_tfidf_converter = None
def inference(sentence):
    global _cached_model
    if _cached_model is None:
        with open(XGBOOST_MODEL_PATH, 'rb') as f:
            _cached_model = pickle.load(f)

    global _cached_tfidf_converter
    if _cached_tfidf_converter is None:
        with open(TFIDF_MODEL_PATH, 'rb') as f:
            _cached_tfidf_converter = pickle.load(f)

    feature = _cached_tfidf_converter.transform(np.array([preprocess(sentence)])).toarray()

    return (_cached_model.predict(feature)[0] - 1).item()


if __name__ == '__main__':
    le = preprocessing.LabelEncoder()
    le.fit(["positive", "neutral", "negative"])

    # Train on pre-labeled airline tweets
    df = pd.read_csv(TRAIN_PATH)
    df = df[['airline_sentiment', 'text']].reset_index().rename(columns={'airline_sentiment': 'sentiment'})
    df.sentiment = le.transform(df.sentiment)
    df['processed_text'] = df['text'].apply(lambda x: preprocess(x))

    # Downsampling Majority Class by removing 80% of negative sentiment
    temp = df
    np.random.seed(10)
    n0 = int(len(df[df.sentiment == 0]) * 0.85)
    drop_indices0 = np.random.choice(df[df.sentiment == 0].index, n0, replace=False)
    df_downsampled = temp.drop(drop_indices0)

    n2 = int(len(df[df.sentiment == 2]) * 0.3)
    drop_indices2 = np.random.choice(df[df.sentiment == 2].index, n2, replace=False)
    df_downsampled = df_downsampled.drop(drop_indices2)

    tfidfconverter = TfidfVectorizer(max_features=408, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
    X = tfidfconverter.fit_transform(df_downsampled.processed_text.values).toarray()
    with open(TFIDF_MODEL_PATH, 'wb') as f:
        pickle.dump(tfidfconverter, f)

    y = df_downsampled.sentiment
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    xgb = XGBClassifier()
    xgb.fit(X_train, y_train)
    with open(XGBOOST_MODEL_PATH, 'wb') as f:
        pickle.dump(xgb, f)
    y_pred = xgb.predict(X_test)
    predictions = [round(value) for value in y_pred]
    print("Accuracy on test set:", accuracy_score(y_test, predictions))

    # Evaluate on 1000 hand-labeled trump tweets
    trump = pd.read_csv(EVALUATION_PATH).dropna()
    trump.Label = trump.Label.replace(1.0, 2)  # 1 --> 2 - positive
    trump.Label = trump.Label.replace(0.0, 1)  # 0 --> 1 - neutral
    trump.Label = trump.Label.replace(-1.0, 0)  # -1 --> 0 - negative
    trump['processed_content'] = trump['Content'].apply(lambda x: preprocess(str(x)))
    # tfidfconverter = TfidfVectorizer(max_features=500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
    T = tfidfconverter.transform(trump.processed_content.values).toarray()
    y_trump = [int(x) for x in list(trump.Label)]
    y_trump_pred = xgb.predict(T)
    predictions = [int(round(value)) for value in y_trump_pred]
    print("Accuracy on Trump Tweets evaluation set:", accuracy_score(y_trump, predictions))
