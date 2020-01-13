# from decouple import config
import json
import requests

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
# nltk.download('punkt')
from textblob import TextBlob

def score_sentiment(tweet):
        '''Extract sentiment (total and average) from  multi-sentence string, sentence by sentence'''
        text = tweet
        blob = TextBlob(text)
        return blob.sentiment.polarity

def scale_sentiments(sentiments):
    '''
    Use QuantileTransformer to convert sentiment score to value between 0 and 100
    input: initial Sentiment Score pandas Series
    returns: scaled Sentiment Score pandas Series
    '''
    scaler = QuantileTransformer()
    scaler.fit_transform(sentiments)
    sentiments = [score*100 for score in sentiments]
    return pd.Series(sentiments)